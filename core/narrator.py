"""
Narrator enforces the voice of Veil Town.

Rules:
- No reassurance
- No jokes
- No casual language
- Short, restrained sentences
- Institutional tone
"""

class Narrator:
    @staticmethod
    def opening():
        return (
            "Veil Town opens.\n"
            "The streets are quiet.\n"
            "Type /join to enter."
        )

    @staticmethod
    def join(name: str):
        return f"{name} enters the town."

    @staticmethod
    def begin_public():
        return (
            "The town settles.\n"
            "Doors close.\n"
            "Conversation grows careful."
        )

    @staticmethod
    def insufficient_players():
        return "The town requires at least five participants."

    @staticmethod
    def role_dm(role: str):
        return (
            "You have been assigned an identity.\n\n"
            f"Role: {role}\n\n"
            "Do not reveal this.\n"
            "The town is listening."
        )
