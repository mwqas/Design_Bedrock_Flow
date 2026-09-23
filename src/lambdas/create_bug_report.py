import json
import os
import uuid
from datetime import datetime, timezone

import boto3

TABLE_NAME = os.environ["TABLE_NAME"]
table = boto3.resource("dynamodb").Table(TABLE_NAME)

REQUIRED_FIELDS = ("description", "stepsToReproduce", "environment")


def _coerce_payload(event):
    """Accept a direct dict, JSON body, or a small Agent/Flow-style wrapper."""
    if isinstance(event, str):
        return json.loads(event)

    if not isinstance(event, dict):
        raise ValueError("Event must be a JSON object.")

    if isinstance(event.get("body"), str):
        try:
            body = json.loads(event["body"])
            if isinstance(body, dict):
                return body
        except json.JSONDecodeError:
            pass

    # Direct payload used by the wrapper in this repository.
    if all(k in event for k in REQUIRED_FIELDS):
        return event

    # Common nested locations.
    for key in ("payload", "input", "parameters"):
        value = event.get(key)
        if isinstance(value, dict) and all(k in value for k in REQUIRED_FIELDS):
            return value

    # Agent-style parameter list support.
    params = event.get("parameters")
    if isinstance(params, list):
        payload = {}
        for item in params:
            if isinstance(item, dict) and "name" in item:
                payload[item["name"]] = item.get("value")
        if payload:
            return payload

    return event


def lambda_handler(event, context):
    payload = _coerce_payload(event)

    missing = [name for name in REQUIRED_FIELDS if not str(payload.get(name, "")).strip()]
    if missing:
        return {
            "statusCode": 400,
            "error": "MISSING_FIELDS",
            "missingFields": missing,
        }

    ticket_id = str(uuid.uuid4())
    item = {
        "ticketId": ticket_id,
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "description": str(payload["description"]).strip(),
        "stepsToReproduce": str(payload["stepsToReproduce"]).strip(),
        "environment": str(payload["environment"]).strip(),
        "status": "OPEN",
    }

    table.put_item(Item=item)

    return {
        "statusCode": 200,
        "ticketId": ticket_id,
        "status": "OPEN",
    }
