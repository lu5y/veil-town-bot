from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class Notifier:
    def __init__(self, bot, chat_id):
        self.bot = bot
        self.chat_id = chat_id

    # ----------------------------
    # BASIC OUTPUT
    # ----------------------------
    async def group(self, text):
        await self.bot.send_message(
            chat_id=self.chat_id,
            text=text,
            parse_mode="Markdown"
        )

    async def dm(self, user_id, text, buttons=None):
        await self.bot.send_message(
            chat_id=user_id,
            text=text,
            reply_markup=buttons
        )

    # ----------------------------
    # ROLE ASSIGNMENT
    # ----------------------------
    async def assign_roles(self, session):
        for player in session.players.values():
            await self.dm(
                player.user_id,
                f"🕯 **Your role**\n\n"
                f"You are **{player.role.name}**.\n\n"
                f"{player.role.description}"
            )

    # ----------------------------
    # NIGHT ACTIONS
    # ----------------------------
    async def open_night_actions(self, session):
        for player in session.alive_players():
            if not player.role.has_night_action:
                continue

            buttons = self._build_target_buttons(
                session,
                callback_prefix="night",
                exclude=player.user_id
            )

            await self.dm(
                player.user_id,
                "🌑 **Night Action**\n"
                "Choose one target.\n"
                "Your decision is final.",
                buttons
            )

    async def resolve_night(self, session):
        result = session.resolve_night()
        if result:
            await self.group(result)

    # ----------------------------
    # DAWN
    # ----------------------------
    async def announce_dawn(self, session):
        deaths = session.last_night_deaths()

        if not deaths:
            await self.group(
                "🌅 **Dawn breaks.**\n"
                "Everyone returns — for now."
            )
            return

        for player in deaths:
            await self.group(
                f"🩸 **{player.name} is dead.**\n"
                "No explanation is given."
            )

    # ----------------------------
    # VOTING
    # ----------------------------
    async def open_voting(self, session):
        for player in session.alive_players():
            buttons = self._build_target_buttons(
                session,
                callback_prefix="vote",
                exclude=player.user_id
            )

            await self.dm(
                player.user_id,
                "⚖️ **Judgment**\n"
                "Choose who must be cast out.",
                buttons
            )

    async def resolve_votes(self, session):
        executed = session.resolve_votes()

        if not executed:
            await self.group(
                "⚖️ **Judgment passes.**\n"
                "No one is executed."
            )
            return

        await self.group(
            f"⚖️ **Judgment is passed.**\n"
            f"**{executed.name} is executed.**"
        )

    # ----------------------------
    # END GAME
    # ----------------------------
    async def announce_winner(self, session):
        await self.group(session.endgame_summary())

    # ----------------------------
    # BUTTON UTILS
    # ----------------------------
    def _build_target_buttons(self, session, callback_prefix, exclude=None):
        rows = []

        for player in session.alive_players():
            if exclude and player.user_id == exclude:
                continue

            rows.append([
                InlineKeyboardButton(
                    text=player.name,
                    callback_data=f"{callback_prefix}:{player.user_id}"
                )
            ])

        return InlineKeyboardMarkup(rows)
