import asyncio
import logging
from datetime import datetime
from enum import Enum, auto
from config import TEST_MODE, MIN_PLAYERS
from game.roles import Faction
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest # Import error handling

# Setup logger to see errors in Railway console
logger = logging.getLogger(__name__)

class Phase(Enum):
    LOBBY = auto()
    NIGHT = auto()
    DISCUSSION = auto()
    VOTING = auto()
    GAME_OVER = auto()

class GameEngine:
    def __init__(self, state, notifier):
        self.state = state
        self.notifier = notifier
        self.phase = Phase.LOBBY
        self.task = None
        self.lobby_started_at = None
        self.lobby_message_id = None

    async def start_lobby(self, message_id):
        self.lobby_message_id = message_id
        self.lobby_started_at = datetime.now()
        # Start the update loop
        self.task = asyncio.create_task(self._lobby_loop())

    def get_time_left(self):
        if not self.lobby_started_at:
            return 120
        elapsed = (datetime.now() - self.lobby_started_at).seconds
        duration = 120
        return max(0, duration - elapsed)

    async def _lobby_loop(self):
        from core.narrator import Narrator
        
        while self.phase == Phase.LOBBY:
            try:
                time_left = self.get_time_left()
                names = [p.name for p in self.state.players.values()]
                
                join_btn = InlineKeyboardMarkup([[InlineKeyboardButton("Join Veil Town", callback_data="join")]])
                
                # Try to edit the message
                await self.notifier.bot.edit_message_text(
                    chat_id=self.state.chat_id,
                    message_id=self.lobby_message_id,
                    text=Narrator.opening(names, time_left),
                    reply_markup=join_btn,
                    parse_mode='Markdown'
                )
            except BadRequest as e:
                # THIS FIXES THE STUCK TIMER
                if "message is not modified" in str(e).lower():
                    pass # Ignore this specific error, it just means time didn't change enough yet
                else:
                    logger.error(f"Lobby UI Error: {e}")
            except Exception as e:
                logger.error(f"Critical Loop Error: {e}")

            # Auto-Start Logic
            if time_left <= 0:
                if len(self.state.players) >= MIN_PLAYERS:
                    await self.start_game()
                    return
                else:
                    self.lobby_started_at = datetime.now() # Reset timer
            
            await asyncio.sleep(5)

    async def force_start(self):
        # Cancel the timer loop so it doesn't fight the game start
        if self.task:
            self.task.cancel()
            
        if self.phase == Phase.LOBBY:
            await self.start_game()

    async def start_game(self):
        self.phase = Phase.ROLE_ASSIGNMENT
        self.state.assign_roles()
        await self.notifier.send_roles(self.state)
        await self._run_night()

    async def _run_night(self):
        self.phase = Phase.NIGHT
        from core.narrator import Narrator
        
        self.state.reset_daily()
        await self.notifier.group(Narrator.night_start())
        await self.notifier.night_controls(self.state)
        
        await asyncio.sleep(10 if TEST_MODE else 45)
        await self._resolve_night()

    async def _resolve_night(self):
        from core.narrator import Narrator
        deaths = []
        
        # Watcher Logic
        for uid, action in self.state.night_actions.items():
            actor = self.state.players[uid]
            if actor.role_key == "Watcher":
                target_id = action['target']
                target = self.state.players.get(target_id)
                if target:
                    target_acted = target_id in self.state.night_actions
                    msg = Narrator.watcher_result(target.name, target_acted)
                    await self.notifier.dm(uid, msg)

        # Guardian Logic
        for uid, action in self.state.night_actions.items():
            if self.state.players[uid].role_key == "Guardian":
                target = self.state.players.get(action['target'])
                if target: target.is_protected = True

        # Shade Logic
        for uid, action in self.state.night_actions.items():
            actor = self.state.players[uid]
            if actor.role_key == "Shade":
                target = self.state.players.get(action['target'])
                if target and not target.is_protected:
                    target.is_alive = False
                    deaths.append((target.name, target.role.name))

        await self.notifier.group(Narrator.night_end(deaths))
        if self._check_win(): return
        await self._run_discussion()

    async def _run_discussion(self):
        self.phase = Phase.DISCUSSION
        from core.narrator import Narrator
        duration = 15 if TEST_MODE else 90
        await self.notifier.group(Narrator.discussion(duration))
        await asyncio.sleep(duration)
        await self._run_voting()

    async def _run_voting(self):
        self.phase = Phase.VOTING
        from core.narrator import Narrator
        await self.notifier.group(Narrator.voting_start())
        await self.notifier.voting_controls(self.state)
        await asyncio.sleep(15 if TEST_MODE else 45)
        await self._resolve_votes()

    async def _resolve_votes(self):
        counts = {}
        for target_id in self.state.votes.values():
            counts[target_id] = counts.get(target_id, 0) + 1
            
        executed = None
        if counts:
            victim_id = max(counts, key=counts.get)
            if counts[victim_id] > len(self.state.votes) / 2: 
                victim = self.state.players[victim_id]
                victim.is_alive = False
                executed = (victim.name, victim.role.name)

        from core.narrator import Narrator
        await self.notifier.group(Narrator.execution_result(executed[0] if executed else None, executed[1] if executed else None))
        if self._check_win(): return
        await self._run_night()

    def _check_win(self):
        alive_veil = sum(1 for p in self.state.players.values() if p.role.faction == Faction.VEIL and p.is_alive)
        alive_total = sum(1 for p in self.state.players.values() if p.is_alive)
        
        if alive_veil == 0:
            asyncio.create_task(self.notifier.group("🏁 **Town Wins.**"))
            self.phase = Phase.GAME_OVER
            return True
        if alive_veil >= alive_total / 2:
            asyncio.create_task(self.notifier.group("🏁 **The Veil Consumes.**"))
            self.phase = Phase.GAME_OVER
            return True
        return False
