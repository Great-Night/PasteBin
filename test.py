import asyncio

import PasteBin

async def main():
    pastebin = PasteBin.PasteBin(PasteBin.expire.Month.One, content="Hello :D")
    await pastebin.generate()
    print(pastebin.status)
    print(pastebin.url)
    print(pastebin.raw)

if __name__ == '__main__':
    asyncio.run(main())