from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from core.narrator import Narrator

class Notifier:
    def __init__(self, bot, chat_id):
        self.bot = bot
        self.chat_id = chat_id

    async def group(self, text):
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=text, parse_mode='Markdown')
        except:
            pass # Fail silently as per rules

    async def dm(self, user_id, text, keyboard=None):
        try:
            await self.bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard, parse_mode='Markdown')
        except:
            pass

    async def send_roles(self, state):
        for p in state.players.values():
            await self.dm(p.user_id, Narrator.role_dm(p.role))

    async def night_controls(self, state):
        alive = [p for p in state.players.values() if p.is_alive]
        
        for p in state.players.values():
            if not p.is_alive or not p.role.has_night_action:
                continue
                
            # Filter targets (self-targeting usually disabled)
            targets = [t for t in alive if t.user_id != p.user_id]
            
            rows = []
            for t in targets:
                rows.append([InlineKeyboardButton(f"{t.name}", callback_data=f"night:{t.user_id}")])
            
            await self.dm(p.user_id, "Select your target:", InlineKeyboardMarkup(rows))

    async def voting_controls(self, state):
        alive = [p for p in state.players.values() if p.is_alive]
        rows = []
        for t in alive:
            rows.append([InlineKeyboardButton(t.name, callback_data=f"vote:{t.user_id}")])
            
        # Send a centralized voting pad to the group
        await self.bot.send_message(
            chat_id=self.chat_id,
            text="Who do you condemn?",
            reply_markup=InlineKeyboardMarkup(rows)
        )
