import os

# This line fetches the token from the environment.
# If it can't find one, it will crash (which is good, because it means you forgot to set it).
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Set this to False for the real game (slow timing), True for testing (fast timing)
TEST_MODE = os.getenv("TEST_MODE", "False").lower() == "true"

# Game Constants
MIN_PLAYERS = 1 if TEST_MODE else 5
