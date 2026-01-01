import os

# Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TOKEN_HERE")
TEST_MODE = os.getenv("TEST_MODE", "True").lower() == "true"

# Mechanics
MIN_PLAYERS = 1 if TEST_MODE else 5
