from redis import Redis

from aep import RealAEP
from service import Service

redis = Redis(host='localhost', port=6379, db=0)
aep = RealAEP(redis)
service = Service(redis, aep)


def lambda_handler(full_event, context):
    event = full_event["body"]
    # event is the usefull stuff

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
