import random
from .roles import ROLES, Faction

class Player:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.role_key = None # String key from ROLES dict
        self.is_alive = True
        self.targeted_count = 0 # For Stranger
        self.is_protected = False # For Guardian

    @property
    def role(self):
        return ROLES[self.role_key] if self.role_key else None

class GameState:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.players = {} # user_id -> Player
        self.votes = {}   # voter_id -> target_id
        self.night_actions = {} # actor_id -> {type: str, target: int}
        self.night_count = 0
        self.winner = None
        self.history = [] # For Archivist

    def assign_roles(self):
        keys = list(self.players.keys())
        random.shuffle(keys)
        count = len(keys)
        
        # --- SAFE ROLE LIST ---
        # These are the only roles that function 100% right now.
        # As you fix more roles (like Whisperer), add them to this list.
        role_pool = ["Shade", "Watcher", "Guardian"] 
        
        # If we have more players than special roles, fill with Citizens
        while len(role_pool) < count:
            role_pool.append("Citizen")
            
        for i, uid in enumerate(keys):
            # Assign roles safely
            role_name = role_pool[i] if i < len(role_pool) else "Citizen"
            self.players[uid].role_key = role_name

    def record_night_action(self, actor_id, target_id, action_type):
        if self.players[actor_id].is_alive:
            self.night_actions[actor_id] = {"target": target_id, "type": action_type}
            
            target = self.players.get(target_id)
            if target:
                target.targeted_count += 1

    def reset_daily(self):
        self.votes = {}
        self.night_actions = {}
        for p in self.players.values():
            p.is_protected = False
