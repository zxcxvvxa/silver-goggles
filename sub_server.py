import base64
import asyncio
from aiohttp import web

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

SNI_HOST = "firebaseremoteconfigrealtime.googleapis.com"
TARGET_PORT = 443

# Exact SSH link string
EXACT_SSH_LINK = (
    "ssh://cxlvin:cxlvin@firebaseremoteconfigrealtime.googleapis.com:443"
    "?KUX3sw04Vw3D4VZXnUUdxzm0ktSn8qvoPZ3hvirbN91tTqyY31h2V7XVKv73sB2Iq1Ien3DZ4YdTXcLkzxHX2C6Zqm2PL+v2yXb0zBDM8Os8kUjdJaB3nqafX1ffGuaRkmQSQmVVgKWe5GOYBZdTtqjnXiYz2zTjOgTxNl0B/9VFkGkqaxwznWdyY91SDIg1Kp7J95dv2LKhJiBpLPEvEYdj0xK1bXw7erwcSzEmmfbodvu/LLi/KyMjiiRm+S64#ssh-ws"
)

async def handle_sub(request: web.Request):
    # Auto-detect Cloud Run .run.app host domain from request headers
    host_header = (
        request.headers.get("X-Forwarded-Host") or 
        request.headers.get("Host") or 
        "127.0.0.1"
    )
    
    # Strip port number if present
    run_app_host = host_header.split(":")[0]

    # VLESS URI with auto-detected .run.app domain set in the host parameter
    vless_link = (
        f"vless://cxlvin777@{SNI_HOST}:{TARGET_PORT}"
        f"?encryption=none&type=ws&headerType=none"
        f"&path=%2FCxlvinVlWS%3Fed%3D2560&security=tls"
        f"&host={run_app_host}&sni={SNI_HOST}#vless-ws"
    )

    # Combine configurations and encode to Base64
    raw_content = f"{vless_link}\n{EXACT_SSH_LINK}\n"
    encoded_sub = base64.b64encode(raw_content.encode("utf-8")).decode("utf-8")

    return web.Response(
        text=encoded_sub,
        content_type="text/plain; charset=utf-8",
        headers={
            "Subscription-Userinfo": "upload=0; download=0; total=107374182400; expire=0",
            "Profile-Update-Interval": "24",
            "Cache-Control": "no-cache, no-store, must-revalidate"
        }
    )

def init_app():
    app = web.Application()
    app.router.add_get('/sub', handle_sub)
    return app

if __name__ == '__main__':
    app = init_app()
    web.run_app(app, host='127.0.0.1', port=3000)
