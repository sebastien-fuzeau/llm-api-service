import time
from collections import defaultdict, deque
from typing import Deque


class RateLimiter:
    """
    Rate limiter simple par clé (ex: IP).
    Implémentation: sliding window en mémoire.
    """

    def __init__(self, max_requests: int, window_seconds: int) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict[str, Deque[float]] = defaultdict(deque)

    def allow(self, key: str) -> bool:
        """
        Retourne True si la requête est autorisée, False sinon.
        """
        now = time.time()
        q = self.requests[key]

        # Nettoyage des requêtes hors fenêtre
        while q and q[0] < now - self.window_seconds:
            q.popleft()

        if len(q) >= self.max_requests:
            return False

        q.append(now)
        return True
