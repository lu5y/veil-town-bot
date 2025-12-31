# narrative/announcements.py
# Public announcements shown in the group chat

def announce_lobby_open():
    return (
        "🕯️ **A ritual begins.**\n\n"
        "The town gathers.\n"
        "Use /join to enter the game."
    )


def announce_lobby_extended():
    return (
        "⏳ **The ritual is delayed.**\n\n"
        "The town waits for more souls."
    )


def announce_game_start():
    return (
        "🕯️ **The Veil closes.**\n\n"
        "Roles have been assigned.\n"
        "Night falls."
    )


def announce_night():
    return (
        "🌑 **Night has fallen.**\n\n"
        "Those who act in secret may now do so."
    )


def announce_dawn(deaths):
    if not deaths:
        return (
            "🌕 **Dawn breaks.**\n\n"
            "Everyone returns.\n"
            "For now."
        )

    text = "🌕 **Dawn breaks.**\n\n"
    for player in deaths:
        text += f"🩸 **{player.name} is dead.**\n"

    return text


def announce_judgment():
    return (
        "⚖️ **Judgment begins.**\n\n"
        "Cast your vote.\n"
        "The town decides."
    )


def announce_execution(player):
    return (
        "⚖️ **Judgment is passed.**\n\n"
        f"🩸 **{player.name} has been executed.**"
    )


def announce_no_execution():
    return (
        "⚖️ **Judgment ends.**\n\n"
        "No one is executed."
    )


def announce_game_over(alive_players):
    text = "🕯️ **The veil has lifted.**\n\n"

    if alive_players:
        text += "**Survivors:**\n"
        for p in alive_players:
            text += f"– {p.name}\n"
    else:
        text += "No one survived.\n"

    return text
