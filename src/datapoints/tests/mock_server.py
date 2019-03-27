from aiohttp import web
import asyncio
import random
import os


async def handle(request):
    await asyncio.sleep(random.randint(0, 1))
    mock_osm_response = {
        'rate': {
            'remaining': 9999,
        },
        'results': [
            {
                'geometry': {
                    'lat': random.uniform(-90, 90),
                    'lng': random.uniform(-90, 90),
                },
                'components': {
                    '_type': 'street',
                    'country': 'Brasil',
                    'country_code': 'br',
                    'state': 'RS',
                    'city': 'Porto Alegre',
                    'suburn': 'Montserrat',
                    'postcode': '90480-003',
                    'road': 'Avenida Carlos Gomes',
                    'house_number': random.randint(1, 10000),
                }
            }
        ]
      }
    return web.json_response(mock_osm_response)


async def init(host, port):
    app = web.Application()
    app.router.add_route('GET', '/', handle)
    app.router.add_route('GET', '/{any}', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()


loop = asyncio.get_event_loop()

host = os.environ.get('MOCK_SERVER_HOST')
port = os.environ.get('MOCK_SERVER_PORT')
loop.run_until_complete(init(host, port))

loop.run_forever()
