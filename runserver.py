import os
import base64
import traceback
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


@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        return response
    except web.HTTPError as e:
        title = e.status_code
        message = e.text
    except Exception as e:
        title = "That's an error"
        message = traceback.format_exc()
    return aiohttp_jinja2.render_template(
        'error.html',
        request=request,
        context={
            'title': title,
            'message': message,
        }
    )


def run():
    app = web.Application(middlewares=[auth_middleware, error_middleware])
    setup_routes(app)
    setup_static_routes(app)
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(str(config.TEMPLATES_DIR)))

    uprint = partial(print, flush=True)
    port = int(os.environ.get('PORT', 8080))

    uprint('Running aiohttp {}'.format(aiohttp.__version__))
    web.run_app(app, print=uprint, port=port)


if __name__ == '__main__':
    run()
