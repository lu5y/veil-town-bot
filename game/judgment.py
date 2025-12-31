from collections import Counter


class Judgment:
    def __init__(self):
        self.votes = {}

    def reset(self):
        self.votes.clear()

    def vote(self, voter_id: int, target_id: int):
        self.votes[voter_id] = target_id

    def resolve(self, players, magistrate_id=None):
        if not self.votes:
            return None

        count = Counter(self.votes.values())
        top, votes = count.most_common(1)[0]

        # Check tie
        tied = [
            pid for pid, c in count.items() if c == votes
        ]

        if len(tied) > 1 and magistrate_id:
            return tied[0]

        return top
