import json
import os

import boto3

TARGET_FUNCTION = os.environ["TARGET_FUNCTION"]
lambda_client = boto3.client("lambda")


def _search_for_value(obj, wanted_keys):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in wanted_keys:
                return value
        for value in obj.values():
            found = _search_for_value(value, wanted_keys)
            if found is not None:
                return found
    elif isinstance(obj, list):
        for item in obj:
            found = _search_for_value(item, wanted_keys)
            if found is not None:
                return found
    return None


def _extract_bug_payload(event):
    # Direct local invocation.
    if isinstance(event, dict) and "bug_payload" in event:
        raw = event["bug_payload"]
    else:
        # Bedrock Flow Lambda events can evolve. Look for the named input first,
        # then a document/content-like string.
        raw = _search_for_value(event, {"bug_payload", "document"})

    if raw is None:
        # As a final fallback, accept the event itself.
        raw = event

    if isinstance(raw, str):
        raw = raw.strip()
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {"status": "NEEDS_INFO", "message": raw}

    if isinstance(raw, dict):
        return raw

    raise ValueError("Could not parse bug payload from Flow event.")


def _decode_lambda_payload(response):
    payload = response["Payload"].read()
    if not payload:
        return {}
    decoded = json.loads(payload)
    if isinstance(decoded, dict) and isinstance(decoded.get("body"), str):
        try:
            body = json.loads(decoded["body"])
            if isinstance(body, dict):
                return {**decoded, **body}
        except json.JSONDecodeError:
            pass
    return decoded


def _find_ticket_id(obj):
    if isinstance(obj, dict):
        if obj.get("ticketId"):
            return obj["ticketId"]
        for value in obj.values():
            found = _find_ticket_id(value)
            if found:
                return found
    elif isinstance(obj, list):
        for item in obj:
            found = _find_ticket_id(item)
            if found:
                return found
    return None


def lambda_handler(event, context):
    try:
        bug = _extract_bug_payload(event)

        if str(bug.get("status", "")).upper() == "NEEDS_INFO":
            return bug.get("message") or (
                "Please provide the missing bug description, steps to reproduce, "
                "or environment information."
            )

        required = ("description", "stepsToReproduce", "environment")
        missing = [key for key in required if not str(bug.get(key, "")).strip()]
        if missing:
            return "Please provide the missing information: " + ", ".join(missing) + "."

        payload = {key: bug[key] for key in required}

        response = lambda_client.invoke(
            FunctionName=TARGET_FUNCTION,
            InvocationType="RequestResponse",
            Payload=json.dumps(payload).encode("utf-8"),
        )

        result = _decode_lambda_payload(response)

        if response.get("FunctionError"):
            return (
                "I collected your bug details, but the support ticket could not "
                "be created. Please contact human support."
            )

        ticket_id = _find_ticket_id(result)
        if ticket_id:
            return (
                "Your bug report has been created successfully. "
                f"Your ticket ID is {ticket_id}. "
                "The ticket status is OPEN."
            )

        return (
            "Your bug report was submitted successfully, but the ticket ID "
            "could not be retrieved."
        )

    except Exception as exc:
        print("WRAPPER ERROR:", repr(exc))
        return (
            "I collected your bug details, but I couldn't create the support "
            "ticket. Please contact human support."
        )
