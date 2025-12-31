# core/engine.py
# Veil Town – Core Game Engine
# Self-contained, phase-driven, production safe

import asyncio
import time
from typing import Dict, Optional


class GameEngine:
    """
    Central authority for all game logic.
    Handles lobby, phases, timers, and state.
    """

    # ---- CONFIG ----
    MIN_PLAYERS = 5
    MAX_PLAYERS = 15

    LOBBY_DURATION = 90        # seconds
    LOBBY_EXTENSION = 60       # seconds (once)
    NIGHT_DURATION = 60
    DAY_DURATION = 90
    JUDGMENT_DURATION = 60

    # ---- INIT ----
    def __init__(self):
        # chat_id -> session
        self.sessions: Dict[int, dict] = {}
        self._locks: Dict[int, asyncio.Lock] = {}

    # ======================================================
    # SESSION HELPERS
    # ======================================================

    def has_game(self, chat_id: int) -> bool:
        return chat_id in self.sessions

    def get_session(self, chat_id: int) -> Optional[dict]:
        return self.sessions.get(chat_id)

    def _lock(self, chat_id: int) -> asyncio.Lock:
        if chat_id not in self._locks:
            self._locks[chat_id] = asyncio.Lock()
        return self._locks[chat_id]

    # ======================================================
    # GAME CREATION / LOBBY
    # ======================================================

    def create_game(self, chat_id: int):
        if self.has_game(chat_id):
            return

        self.sessions[chat_id] = {
            "phase": "lobby",
            "players": {},           # user_id -> user
            "created_at": time.time(),
            "lobby_extended": False,
            "task": None,
        }

        # start lobby timer
        self.sessions[chat_id]["task"] = asyncio.create_task(
            self._lobby_timer(chat_id)
        )

    def add_player(self, chat_id: int, user):
        session = self.get_session(chat_id)
        if not session:
            return

        if session["phase"] != "lobby":
            return

        if len(session["players"]) >= self.MAX_PLAYERS:
            return

        session["players"][user.id] = user

    def extend_lobby(self, chat_id: int) -> bool:
        session = self.get_session(chat_id)
        if not session:
            return False

        if session["phase"] != "lobby":
            return False

        if session["lobby_extended"]:
            return False

        session["lobby_extended"] = True
        session["created_at"] += self.LOBBY_EXTENSION
        return True

    def force_start(self, chat_id: int) -> bool:
        session = self.get_session(chat_id)
        if not session:
            return False

        if session["phase"] != "lobby":
            return False

        if len(session["players"]) < self.MIN_PLAYERS:
            return False

        task = session.get("task")
        if task:
            task.cancel()

        asyncio.create_task(self._start_game(chat_id))
        return True

    # ======================================================
    # LOBBY TIMER
    # ======================================================

    async def _lobby_timer(self, chat_id: int):
        try:
            await asyncio.sleep(self.LOBBY_DURATION)
            await self._start_game(chat_id)
        except asyncio.CancelledError:
            return

    async def _start_game(self, chat_id: int):
        async with self._lock(chat_id):
            session = self.get_session(chat_id)
            if not session:
                return

            if len(session["players"]) < self.MIN_PLAYERS:
                # not enough players → kill session
                self.sessions.pop(chat_id, None)
                return

            session["phase"] = "night"
            session["task"] = asyncio.create_task(
                self._phase_cycle(chat_id)
            )

    # ======================================================
    # PHASE CYCLE
    # ======================================================

    async def _phase_cycle(self, chat_id: int):
        try:
            while self.has_game(chat_id):
                await self._run_night(chat_id)
                await self._run_day(chat_id)
                await self._run_judgment(chat_id)
        except asyncio.CancelledError:
            return

    async def _run_night(self, chat_id: int):
        async with self._lock(chat_id):
            session = self.get_session(chat_id)
            if not session:
                return
            session["phase"] = "night"

        await asyncio.sleep(self.NIGHT_DURATION)

    async def _run_day(self, chat_id: int):
        async with self._lock(chat_id):
            session = self.get_session(chat_id)
            if not session:
                return
            session["phase"] = "day"

        await asyncio.sleep(self.DAY_DURATION)

    async def _run_judgment(self, chat_id: int):
        async with self._lock(chat_id):
            session = self.get_session(chat_id)
            if not session:
                return
            session["phase"] = "judgment"

        await asyncio.sleep(self.JUDGMENT_DURATION)

    # ======================================================
    # STATUS (SAFE READS)
    # ======================================================

    def get_phase(self, chat_id: int) -> Optional[str]:
        session = self.get_session(chat_id)
        if not session:
            return None
        return session["phase"]

    def get_players(self, chat_id: int):
        session = self.get_session(chat_id)
        if not session:
            return {}
        return session["players"]

    def end_game(self, chat_id: int):
        session = self.sessions.pop(chat_id, None)
        if session and session.get("task"):
            session["task"].cancel()
