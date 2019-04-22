import base64
from functools import partial

import jinja2
import aiohttp
import aiohttp_jinja2
from aiohttp import web

import config
from whereisqa import setup_routes, setup_static_routes


def check_access(auth):
    creds = f'{config.AUTH_USERNAME}:{config.AUTH_PASSWORD}'.encode()
    auth_header = (b'Basic ' + base64.b64encode(creds)).decode()
    return auth == auth_header


@web.middleware
async def auth_middleware(request, handler):
    if not check_access(request.headers.get('Authorization', '')):
        raise web.HTTPUnauthorized(headers={'WWW-Authenticate': 'Basic'})

    return await handler(request)


def run():
    app = web.Application(middlewares=[auth_middleware])
    setup_routes(app)
    setup_static_routes(app)
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(str(config.TEMPLATES_DIR)))

    uprint = partial(print, flush=True)
    port = int(config.RUN_PORT)

    uprint('Running aiohttp {}'.format(aiohttp.__version__))
    web.run_app(app, print=uprint, port=port)


if __name__ == '__main__':
    run()
