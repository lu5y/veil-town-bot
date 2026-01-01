class Narrator:
    @staticmethod
    def opening():
        return "Veil Town opens.\nType /join to enter."

    @staticmethod
    def role_dm(role_data):
        return (
            f"**IDENTITY: {role_data.name}**\n\n"
            f"{role_data.description}\n"
            f"Goal: {role_data.win_condition}\n\n"
            "Do not reveal this."
        )

    @staticmethod
    def night_start():
        return "🌑 **Night falls.**\nThe town is silent.\nCheck your private messages."

    @staticmethod
    def night_end(deaths):
        if not deaths:
            return "The sun rises. The streets are empty, but clean."
        
        text = "🩸 **Dawn.**\n"
        for name, role in deaths:
            text += f"{name} was found dead. They were the {role}.\n"
        return text

    @staticmethod
    def discussion(seconds):
        return f"☀️ **Day.**\nSpeak. You have {seconds} seconds."

    @staticmethod
    def voting_start():
        return "🗳️ **Judgment.**\nCast your vote."

    @staticmethod
    def execution_result(name, role):
        if name:
            return f"⚖️ **Judgment delivered.**\n{name} ({role}) has been executed."
        return "The gallows remain empty."
