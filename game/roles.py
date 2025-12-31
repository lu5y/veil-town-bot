class Role:
    def __init__(
        self,
        name: str,
        description: str,
        has_night_action: bool = False,
        can_kill: bool = False,
        can_protect: bool = False,
        can_observe: bool = False,
        priority: int = 0,
    ):
        self.name = name
        self.description = description
        self.has_night_action = has_night_action
        self.can_kill = can_kill
        self.can_protect = can_protect
        self.can_observe = can_observe
        self.priority = priority  # for action resolution order later


# ----------------------------
# CORE ROLES (15 MAX)
# ----------------------------

BOUND_ONE = Role(
    name="Bound One",
    description=(
        "You are bound by something older than this town.\n"
        "Each night, you must choose someone.\n"
        "If you do not act, the Veil will choose for you."
    ),
    has_night_action=True,
    can_kill=True,
    priority=10,
)

DOCTOR = Role(
    name="Doctor",
    description=(
        "You tend to the wounded and delay the inevitable.\n"
        "Each night, choose one person to protect."
    ),
    has_night_action=True,
    can_protect=True,
    priority=5,
)

WATCHER = Role(
    name="Watcher",
    description=(
        "You stay awake when others sleep.\n"
        "Each night, choose someone to observe."
    ),
    has_night_action=True,
    can_observe=True,
    priority=3,
)

MAGISTRATE = Role(
    name="Magistrate",
    description=(
        "Your word carries weight.\n"
        "During judgment, ties bend toward you."
    ),
    has_night_action=False,
)

ARCHIVIST = Role(
    name="Archivist",
    description=(
        "You remember what others forget.\n"
        "You have no power — only memory."
    ),
)

MOURNER = Role(
    name="Mourner",
    description=(
        "You watch the town lose pieces of itself.\n"
        "The dead speak louder to you than the living."
    ),
)

MIDWIFE = Role(
    name="Midwife",
    description=(
        "You have brought life into this world.\n"
        "You cannot stop death."
    ),
)

STRANGER = Role(
    name="Stranger",
    description=(
        "You do not belong here.\n"
        "The town knows it."
    ),
)

SILENT_ONE = Role(
    name="Silent One",
    description=(
        "You survive by saying nothing.\n"
        "Silence does not mean innocence."
    ),
)

CHILD = Role(
    name="Child",
    description=(
        "You see everything without understanding it.\n"
        "The town will protect you — or blame you."
    ),
)

GRAVEDIGGER = Role(
    name="Gravedigger",
    description=(
        "You prepare places for the fallen.\n"
        "You are never surprised."
    ),
)

CONFESSOR = Role(
    name="Confessor",
    description=(
        "People speak to you when they are afraid.\n"
        "Truth is not always helpful."
    ),
)

OUTCAST = Role(
    name="Outcast",
    description=(
        "The town decided long ago not to trust you.\n"
        "Tonight will not change that."
    ),
)

HERBALIST = Role(
    name="Herbalist",
    description=(
        "You work with remedies that may heal or harm.\n"
        "Intent matters less than outcome."
    ),
)

WANDERER = Role(
    name="Wanderer",
    description=(
        "You move while others stay still.\n"
        "Some nights, this saves you."
    ),
)


# ----------------------------
# ROLE POOL
# ----------------------------

ALL_ROLES = [
    BOUND_ONE,
    DOCTOR,
    WATCHER,
    MAGISTRATE,
    ARCHIVIST,
    MOURNER,
    MIDWIFE,
    STRANGER,
    SILENT_ONE,
    CHILD,
    GRAVEDIGGER,
    CONFESSOR,
    OUTCAST,
    HERBALIST,
    WANDERER,
]
