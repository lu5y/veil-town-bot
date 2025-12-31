# narrative/whispers.py
# Private messages (DMs) sent to individual players


def role_reveal(player):
    return (
        "🕯️ **Your Role**\n\n"
        f"You are **{player.role.name}**.\n\n"
        f"{player.role.description}\n\n"
        "This information is yours alone."
    )


def night_action_prompt(role_name):
    return (
        "🌑 **Night Action**\n\n"
        f"As the **{role_name}**, you may choose one target.\n"
        "Your choice is secret and final."
    )


def night_no_action():
    return (
        "🌑 **Night falls.**\n\n"
        "You have no action tonight.\n"
        "Remain silent."
    )


def action_confirmed():
    return (
        "✔️ **Action confirmed.**\n\n"
        "The Veil has recorded your choice."
    )


def vote_prompt():
    return (
        "⚖️ **Judgment**\n\n"
        "Choose who should be cast out.\n"
        "Your vote cannot be changed."
    )


def vote_confirmed():
    return (
        "✔️ **Vote recorded.**\n\n"
        "The town will decide."
    )


def observed_result(target_name):
    return (
        "👁 **Observation**\n\n"
        f"You watched **{target_name}** last night.\n"
        "Their actions will be remembered."
    )


def protected_result(target_name):
    return (
        "🛡 **Protection**\n\n"
        f"You protected **{target_name}** last night.\n"
        "Whether it mattered, you may never know."
    )


def killed_result():
    return (
        "🩸 **You are dead.**\n\n"
        "Your part in the town has ended.\n"
        "You may watch, but you may not speak."
    )
