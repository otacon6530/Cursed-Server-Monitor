class EventBus:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_type, callback):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type, callback):
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(callback)

    def publish(self, event_type, data=None):
        for callback in self._subscribers.get(event_type, []):
            callback(data)
event_bus = EventBus()