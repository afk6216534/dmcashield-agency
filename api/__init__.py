from backend.main_simple import app

def handler(event, context):
    import json
    from fastapi import Request

    # Convert Vercel event to FastAPI request
    request = Request(scope={
        "type": "http",
        "method": event.get("httpMethod", "GET"),
        "headers": event.get("headers", {}),
        "path": event.get("path", ""),
        "queryStringParameters": event.get("queryStringParameters", {}),
        "body": event.get("body"),
    })

    # FastAPI app
    response = app.handle_request(request)
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": "JARVIS endpoint ready"})
    }