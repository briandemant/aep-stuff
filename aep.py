from abc import ABC, abstractmethod
from uuid import uuid4

from redis import Redis


class AEP(ABC):
    def __init__(self, redis: Redis):
        self.redis = redis

    @abstractmethod
    def create_api(self) -> str:
        pass

    @abstractmethod
    def call_api(self, flow_id: str, data: dict):
        pass

    @abstractmethod
    def get_flow_id(self):
        pass


class RealAEP:
    def create_api(self) -> str:
        return "new_flow_id"

    def call_api(self, flow_id: str, data: dict):
        pass

    def get_flow_id(self):
        return "new_flow_id"


fake_map = {}


class FakeAEP:
    def create_api(self, concat_id) -> str:
        flow_id = str(uuid4())
        fake_map[concat_id] = flow_id
        return flow_id

    def call_api(self, flow_id: str, data: dict):
        self.redis.lpush("output", data)
        pass

    def get_flow_id(self, concat_id):
        return fake_map.get(concat_id)
