# telegram_ui/messages.py
# Message formatting helpers for Veil Town UI


def bold(text: str) -> str:
    return f"**{text}**"


def section(title: str, body: str) -> str:
    return f"{bold(title)}\n\n{body}"


def simple_notice(text: str) -> str:
    return f"ℹ️ {text}"


def error(text: str) -> str:
    return f"❗ {text}"


def success(text: str) -> str:
    return f"✔️ {text}"


def player_list(players):
    if not players:
        return "No players."

    text = ""
    for p in players:
        text += f"• {p.name}\n"
    return text


def lobby_status(players, min_players):
    return (
        "🕯️ **Lobby Status**\n\n"
        f"Players joined: {len(players)} / {min_players}\n\n"
        f"{player_list(players)}"
    )
