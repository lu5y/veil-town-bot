class Narrator:
    @staticmethod
    def opening(player_names, time_left):
        # Format: Vertical list like in your screenshot
        if not player_names:
            list_text = "(Waiting for players...)"
        else:
            # Creates a vertical list with bullet points
            list_text = "\n".join([f"• {name}" for name in player_names])

        return (
            "🕯️ **Veil Town opens.**\n"
            "The fog descends. The streets are empty.\n\n"
            f"#players: {len(player_names)}\n"
            f"{list_text}\n\n"
            f"⏳ **Time Remaining:** {time_left}s\n\n"
            "Press **Join** to sign your name."
        )

    @staticmethod
    def role_dm(role_data):
        return (
            f"📜 **IDENTITY: {role_data.name}**\n\n"
            f"_{role_data.description}_\n\n"
            f"🏆 **Goal:** {role_data.win_condition}\n"
            "-----------------------------\n"
            "Do not reveal this card.\n"
            "The town is listening."
        )

    @staticmethod
    def night_start():
        return "🌑 **Night falls.**\nDoors are barred. Check your DMs."

    @staticmethod
    def night_end(deaths):
        if not deaths:
            return "☀️ **Dawn breaks.**\nNo one died last night."
        text = "🩸 **Tragedy at dawn.**\n"
        for name, role in deaths:
            text += f"💀 **{name}** ({role}) dead.\n"
        return text

    @staticmethod
    def watcher_result(target_name, acted):
        if acted:
            return f"👁️ **Observation:**\n{target_name} left their home."
        return f"👁️ **Observation:**\n{target_name} stayed home."

    @staticmethod
    def discussion(seconds):
        return f"☀️ **Day.**\nDiscuss. You have {seconds}s."

    @staticmethod
    def voting_start():
        return "⚖️ **Judgment.**\nVote now."

    @staticmethod
    def execution_result(name, role):
        if name:
            return f"🪓 **Executed:** {name} ({role})"
        return "⚖️ **No one was executed.**"
    
    @staticmethod
    def help_text(phase):
        return "Survive."
