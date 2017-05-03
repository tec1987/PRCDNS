import aiohttp
import asyncio
import async_timeout

@asyncio.coroutine
def fetch(session, url):
    with async_timeout.timeout(10):
        response = yield from session.get(url)
        try:
            return (yield from response.text())
        except Exception as e:
            response.close()
            raise e
        finally:
            yield from response.release()

@asyncio.coroutine
def main(loop):
    with aiohttp.ClientSession(loop=loop, connector = aiohttp.TCPConnector(verify_ssl=False)) as session:
        html = yield from fetch(session, 'https://dns.google.com/resolve?name=g.cn')
        print(html)

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))