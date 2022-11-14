from contextlib import suppress
from dataclasses import dataclass
import atexit

from aiohttp import ClientSession, ClientResponse
from bs4 import BeautifulSoup



@dataclass
class expire(str):
    @dataclass
    class Week:
        One: str = "604800"
        Two: str = "1209600"

    @dataclass
    class Month:
        One: str = "2592000"
        Two: str = "7776000"
        Six: str = "15780000"

    @dataclass
    class Year:
        One: str = "31536000"



class PasteBin:
    def __init__(self, Expire: str = expire.Week.Two, content: str = "", description: str = "", name: str = ""):
        self.status = None
        self.request = ClientResponse
        self.url = "https://paste.ee/"
        self.session = ClientSession(requote_redirect_url=True)
        self.Payload = lambda token: {
            "_token": token,
            "expiration": Expire,
            "expiration_views": "",
            "description": description,
            "paste[section1][name]": name,
            "paste[section1][syntax]": "text",
            "paste[section1][contents]": content,
            "fixlines": True,
            "jscheck": True,
            "jscheck": True
        }
        atexit.register(self._shutdown)

    def _shutdown(self):
        asyncio.run(self.session.close())

    async def token(self):
        for meta in BeautifulSoup(await (await self.session.get(self.url)).text(), "lxml").find_all("input"):
            with suppress(KeyError):
                if meta['name'] == "_token": return meta['value']

    async def generate(self):
        self.request = await self.session.post("https://paste.ee/paste",
                                               data=self.Payload(await self.token()))
        assert self.request.status == 200, "Server responded with status code %s" % self.request.status
        self.url = str(self.request.url)
        self.status = self.request.status
        await self.session.close()

    async def get_url(self):
        return self.url

    async def get_status(self):
        return self.status
