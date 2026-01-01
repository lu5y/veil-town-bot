from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import Forbidden, BadRequest

class Notifier:
    def __init__(self, bot, chat_id):
        self.bot = bot
        self.chat_id = chat_id

    async def group(self, text, keyboard=None):
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=text, reply_markup=keyboard, parse_mode='Markdown')
        except Exception as e:
            print(f"Group send failed: {e}")

    async def dm(self, user_id, text, keyboard=None):
        try:
            await self.bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard, parse_mode='Markdown')
        except Forbidden:
            # THIS IS THE FIX: If a user blocked the bot, we just print a log and CONTINUE.
            # We do NOT let the game crash.
            print(f"⚠️ Cannot DM user {user_id} - they haven't started the bot.")
        except Exception as e:
            print(f"DM failed for {user_id}: {e}")

    async def send_roles(self, state):
        for p in state.players.values():
            if p.role:
                from core.narrator import Narrator
                await self.dm(p.user_id, Narrator.role_dm(p.role))

    async def night_controls(self, state):
        alive = [p for p in state.players.values() if p.is_alive]
        
        for p in state.players.values():
            # Only send buttons if they have an action AND are alive
            if not p.is_alive or not p.role.has_night_action:
                continue
            
            targets = [t for t in alive if t.user_id != p.user_id]
            rows = []
            for t in targets:
                rows.append([InlineKeyboardButton(f"{t.name}", callback_data=f"night:{t.user_id}")])
            
            # Generic prompt for now (works for all roles)
            await self.dm(p.user_id, "Select your target:", InlineKeyboardMarkup(rows))

    async def voting_controls(self, state):
        alive = [p for p in state.players.values() if p.is_alive]
        rows = []
        for t in alive:
            rows.append([InlineKeyboardButton(t.name, callback_data=f"vote:{t.user_id}")])
            
        await self.group("Who do you condemn?", InlineKeyboardMarkup(rows))
