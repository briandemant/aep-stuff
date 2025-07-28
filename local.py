from redis import Redis

from aep import FakeAEP
from service import Service

redis = Redis(host='localhost', port=6379, db=0)
aep = FakeAEP(redis)
service = Service(redis, aep)



def fast_api_endpoint():
    event = redis.lpop("test_queue", 1)
    # event is always only the usefull stuff

    flow_id = service.handle_event(event)
    if flow_id:
        return {
            "statusCode": 200,
            "body": f"Flow ID: {flow_id}"
        }
    else:
        return {
            "statusCode": 500,
            "body": "Failed to handle event"
        }


if __name__ == "__main__":
    print("Starting service")
    print(f"http://localhost:8080")
    uvicorn.run(
        "service:app",
        host="0.0.0.0",
        port=8080,
        workers=1,
        log_level=logging.WARNING,
    )