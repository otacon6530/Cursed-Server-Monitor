from datetime import datetime

class TimeEventManager:
    def __init__(self):
        self.events = []  # Each event: (expiration_time, callback)

    def add_event(self, expiration_time, callback):
        """Add a new event with expiration_time (datetime) and callback (function)."""
        self.events.append((expiration_time, callback))

    def tick(self):
        """Check all events, trigger callbacks for expired ones, and remove them."""
        now = datetime.now()
        expired = []
        for i, (expiration_time, callback) in enumerate(self.events):
            if now >= expiration_time:
                try:
                    callback()
                except Exception as e:
                    print(f"TimeEventManager: Callback error: {e}")
                expired.append(i)
        # Remove expired events
        self.events = [event for idx, event in enumerate(self.events) if idx not in expired]