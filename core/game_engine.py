import asyncio
from enum import Enum, auto
from datetime import datetime, timedelta


class Phase(Enum):
    WAITING = auto()
    ROLE_ASSIGNMENT = auto()
    NIGHT = auto()
    NIGHT_RESOLUTION = auto()
    DAWN = auto()
    DISCUSSION = auto()
    VOTING = auto()
    JUDGMENT = auto()
    GAME_OVER = auto()


class GameEngine:
    def __init__(self, session, notifier):
        """
        session  = GameState (truth storage)
        notifier = object that sends messages (group / dm)
        """
        self.session = session
        self.notifier = notifier
        self.phase = Phase.WAITING
        self.phase_task = None
        self.started_at = None

        # timing (seconds)
        self.MIN_PLAYERS = 6
        self.WAIT_DURATION = 120
        self.EXTENSION_DURATION = 60
        self.NIGHT_DURATION = 45
        self.DISCUSSION_DURATION = 90
        self.VOTING_DURATION = 45

        self.wait_extended = False

    # ----------------------------
    # ENTRY POINT
    # ----------------------------
    async def start_lobby(self):
        self.phase = Phase.WAITING
        self.started_at = datetime.utcnow()

        await self.notifier.group(
            "🕯️ **The Veil stirs…**\n"
            "A new game is forming.\n\n"
            f"Minimum players: **{self.MIN_PLAYERS}**\n"
            "Press **Join** to enter."
        )

        self.phase_task = asyncio.create_task(self._wait_loop())

    # ----------------------------
    # WAITING PHASE
    # ----------------------------
    async def _wait_loop(self):
        while self.phase == Phase.WAITING:
            if len(self.session.players) >= self.MIN_PLAYERS:
                await self._begin_game()
                return

            elapsed = (datetime.utcnow() - self.started_at).seconds
            if elapsed >= self.WAIT_DURATION:
                await self._begin_game()
                return

            await asyncio.sleep(3)

    async def extend_wait(self):
        if self.wait_extended:
            return False

        self.wait_extended = True
        self.started_at += timedelta(seconds=self.EXTENSION_DURATION)

        await self.notifier.group(
            "⏳ **The Veil lingers…**\n"
            "Waiting time extended once."
        )
        return True

    async def force_start(self):
        if self.phase != Phase.WAITING:
            return

        await self.notifier.group(
            "⚖️ **The ritual is forced.**\n"
            "The game begins immediately."
        )
        await self._begin_game()

    # ----------------------------
    # GAME START
    # ----------------------------
    async def _begin_game(self):
        self.phase = Phase.ROLE_ASSIGNMENT

        await self.notifier.group("🎭 **Roles are being assigned…**")

        await self.notifier.assign_roles(self.session)

        await asyncio.sleep(3)
        await self._night_phase()

    # ----------------------------
    # NIGHT
    # ----------------------------
    async def _night_phase(self):
        self.phase = Phase.NIGHT

        await self.notifier.group(
            "🌑 **Night falls.**\n"
            "Close your eyes.\n"
            "Those who act will be summoned."
        )

        await self.notifier.open_night_actions(self.session)

        await asyncio.sleep(self.NIGHT_DURATION)
        await self._resolve_night()

    # ----------------------------
    # NIGHT RESOLUTION
    # ----------------------------
    async def _resolve_night(self):
        self.phase = Phase.NIGHT_RESOLUTION

        await self.notifier.resolve_night(self.session)

        await asyncio.sleep(2)
        await self._dawn()

    # ----------------------------
    # DAWN
    # ----------------------------
    async def _dawn(self):
        self.phase = Phase.DAWN

        await self.notifier.announce_dawn(self.session)

        if self.session.check_win():
            await self._end_game()
            return

        await asyncio.sleep(3)
        await self._discussion()

    # ----------------------------
    # DISCUSSION
    # ----------------------------
    async def _discussion(self):
        self.phase = Phase.DISCUSSION

        await self.notifier.group(
            "☀️ **Day breaks.**\n"
            "Speak carefully.\n"
            f"You have **{self.DISCUSSION_DURATION} seconds**."
        )

        await asyncio.sleep(self.DISCUSSION_DURATION)
        await self._voting()

    # ----------------------------
    # VOTING
    # ----------------------------
    async def _voting(self):
        self.phase = Phase.VOTING

        await self.notifier.open_voting(self.session)

        await asyncio.sleep(self.VOTING_DURATION)
        await self._judgment()

    # ----------------------------
    # JUDGMENT
    # ----------------------------
    async def _judgment(self):
        self.phase = Phase.JUDGMENT

        await self.notifier.resolve_votes(self.session)

        if self.session.check_win():
            await self._end_game()
            return

        await asyncio.sleep(3)
        await self._night_phase()

    # ----------------------------
    # END GAME
    # ----------------------------
    async def _end_game(self):
        self.phase = Phase.GAME_OVER

        await self.notifier.announce_winner(self.session)

        self.session.reset()
