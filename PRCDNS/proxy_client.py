import asyncio
import aiohttp


class ProxyClient:
    """Google DNS Client"""
    proxy = None

    # def __init__(self, proxy=None):
    #     self.proxy = proxy

    @staticmethod
    @asyncio.coroutine
    def fetch(session, url, proxy=None):
        with aiohttp.Timeout(10):
            # http://127.0.0.1:8123
            response = yield from session.get(url, proxy=proxy)
            try:
                return (yield from response.text())
            except Exception as e:
                response.close()
                raise e
            finally:
                yield from response.release()
    @staticmethod
    @asyncio.coroutine
    def query_domain(url, proxy=None):
        with aiohttp.ClientSession(connector = aiohttp.TCPConnector(verify_ssl=False)) as session:
            try:
                return (yield from ProxyClient.fetch(session, url, proxy))
            except Exception as e:
                raise e
            finally:
                yield from session.close()

    @staticmethod
    @asyncio.coroutine
    def get(loop, url):
        with aiohttp.ClientSession(loop=loop, connector = aiohttp.TCPConnector(verify_ssl=False)) as session:
            try:
                return (yield from ProxyClient.fetch(session, url))
            except Exception as e:
                raise e
            finally:
                yield from session.close()

    @staticmethod
    def get_url(url, proxy=None):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(ProxyClient.get(loop, url))
