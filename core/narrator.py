class Narrator:
    @staticmethod
    def opening(count, time_left):
        return (
            "🕯️ **Veil Town opens.**\n"
            "The fog descends. The streets are empty.\n\n"
            f"👥 **Joined:** {count}\n"
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
        return (
            "🌑 **Night falls.**\n"
            "Doors are barred. Candles are blown out.\n"
            "Check your private messages immediately."
        )

    @staticmethod
    def night_end(deaths):
        if not deaths:
            return "☀️ **Dawn breaks.**\nThe cobblestones are dry.\nNo one died last night."
        text = "🩸 **Tragedy at dawn.**\nWe found bodies in the square:\n\n"
        for name, role in deaths:
            text += f"💀 **{name}** was the **{role}**.\n"
        return text

    @staticmethod
    def watcher_result(target_name, acted):
        if acted:
            return f"👁️ **Observation:**\nYou watched {target_name} closely.\nThey left their home tonight."
        return f"👁️ **Observation:**\nYou watched {target_name}.\nThey stayed home."

    @staticmethod
    def discussion(seconds):
        return f"☀️ **The Town Gathers.**\nAccuse. Defend. Lie.\nYou have **{seconds} seconds** before judgment."

    @staticmethod
    def voting_start():
        return "⚖️ **Judgment Time.**\nThe gallows await a decision.\nSelect a name to condemn them."

    @staticmethod
    def execution_result(name, role):
        if name:
            return f"🪓 **Sentence Carried Out.**\n{name} has been executed.\nThey were the **{role}**."
        return "⚖️ **No Majority.**\nThe rope hangs empty today.\nThe town disperses in silence."
    
    @staticmethod
    def help_text(phase):
        from core.game_engine import Phase
        if phase == Phase.LOBBY: return "We are gathering souls. Tell friends to join."
        if phase == Phase.NIGHT: return "It is dark. Check your private chat to act."
        if phase == Phase.DISCUSSION: return "Daylight. Discuss who among you is the traitor."
        if phase == Phase.VOTING: return "The vote is mandatory. Click a button to choose."
        return "The Veil is quiet."
