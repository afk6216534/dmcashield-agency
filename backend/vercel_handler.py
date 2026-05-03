from main_simple import app
import json as json_lib
from starlette.requests import Request
from starlette.responses import Response
import asyncio

def handler(event, context):
    async def run():
        # Convert event to Starlette request
        scope = {
            "type": "http",
            "method": event.get("httpMethod", "GET"),
            "path": event.get("path", "/"),
            "headers": [(k.encode(), v.encode()) for k, v in event.get("headers", {}).items()],
            "query_string": event.get("queryStringParameters", {}),
        }

        body = event.get("body", "")
        if isinstance(body, dict):
            body = json_lib.dumps(body)

        request = Request(scope, receive=lambda: None)

        # Call FastAPI app
        response = await app(request)

        return {
            "statusCode": response.status_code,
            "headers": dict(response.headers),
            "body": response.body.decode() if isinstance(response.body, bytes) else str(response.body)
        }

    return asyncio.get_event_loop().run_until_complete(run())