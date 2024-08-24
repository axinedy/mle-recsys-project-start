import logging


log = logging.getLogger("uvicorn.error")


class EventStore:

    def __init__(self, max_events_per_user=10):

        self.events = {}
        self.max_events_per_user = max_events_per_user

    def put(self, user_id, item_id):
        log.info(f'EventsStore.put {user_id}, {item_id}')
        user_events = self.events[user_id] if user_id in self.events else []
        self.events[user_id] = [item_id] + user_events[: self.max_events_per_user]
        print(self.events)

    def get(self, user_id, k):
        log.info(f'EventsStore.get {user_id}, {k}')
        user_events = self.events[user_id][:k] if user_id in self.events else []
        print(user_events)
        return user_events
