from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def open_voting(self, players):
    keyboard = []

    for p in players:
        keyboard.append([
            InlineKeyboardButton(
                text=f"🗳️ {p.name}",
                callback_data=f"vote:{p.user_id}"
            )
        ])

    await self.app.bot.send_message(
        chat_id=self.chat_id,
        text="🗳️ *Voting Phase*\nChoose one player to condemn.",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
class Notifier:
    def __init__(self, application, chat_id):
        """
        application: telegram.ext.Application
        chat_id: group chat id
        """
        self.app = application
        self.chat_id = chat_id

    # -------------------------------------------------
    # BASIC GROUP MESSAGE
    # -------------------------------------------------
    async def group(self, text):
        await self.app.bot.send_message(
            chat_id=self.chat_id,
            text=text
        )

    # -------------------------------------------------
    # GAME FLOW ANNOUNCEMENTS
    # -------------------------------------------------
    async def announce_game_start(self, min_players):
        await self.group(
            "🕯️ *The Veil stirs…*\n"
            "A new game is forming.\n\n"
            f"Minimum players: {min_players}\n"
            "Press /join to enter."
        )

    async def announce_roles_assigning(self):
        await self.group(
            "🎭 *Roles are being assigned…*\n"
            "Check your private messages."
        )

    async def announce_night(self):
        await self.group(
            "🌑 *Night falls over Veil Town.*\n"
            "Those who act in darkness may now choose."
        )

    async def announce_dawn(self):
        await self.group(
            "🌅 *Dawn breaks.*\n"
            "The town gathers to face the truth."
        )

    async def announce_discussion(self, seconds):
        await self.group(
            f"💬 *Discussion Phase*\n"
            f"You have {seconds} seconds to speak."
        )

    async def open_voting(self, alive_players):
        await self.group(
            "🗳️ *Voting has begun.*\n"
            "Choose wisely."
        )

    async def resolve_votes(self, executed_player=None):
        if executed_player:
            await self.group(
                f"⚖️ *Judgment is passed.*\n"
                f"**{executed_player.name}** has been executed."
            )
        else:
            await self.group(
                "⚖️ *Judgment fails.*\n"
                "No consensus was reached."
            )

    async def announce_winner(self, winning_faction):
        await self.group(
            f"🏁 *Game Over*\n"
            f"**{winning_faction}** has won the game."
        )
