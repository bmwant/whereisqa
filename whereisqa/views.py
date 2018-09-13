import aiohttp_jinja2
from aiohttp import web
from aiohttp import hdrs

import config
from whereisqa.instances import create_inventory
from whereisqa.utils import logger


@aiohttp_jinja2.template('index.html')
async def index(request):
    logger.info('Accessing index page')
    envs = create_inventory()
    return {
        'envs': envs,
    }
