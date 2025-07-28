from aep import AEP


class Service:
    def __init__(self, redis: dict, aep: AEP):
        self.redis = redis
        self.aep = aep

    def save_for_later(self, event: dict):
        concat_id = self.concat_id(event)
        self.redis.lpush("deadletter", event)
        return concat_id

    def concat_id(self, event):
        return f"{event['userId']}_{event['profileId']}"

    def handle_event(self, event: dict):
        concat_id = self.concat_id(event)
        flow_id = self.aep.get_flow_id(concat_id)
        if not flow_id:
            flow_id = self.aep.create_api(concat_id)
            if not flow_id:
                self.save_for_later(event)
                return None

        try:
            self.aep.call_api(flow_id, event)
        except Exception as e:
            print(f"Error calling API: {e}")
            self.save_for_later(event)
            return None


