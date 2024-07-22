import asyncio
import os

import aiohttp

from db import RatesDatabase
from schema import ExchangeRates


CURRENCY_URL = "https://cbr.ru/scripts/XML_daily.asp"


async def main():
    async with (
        aiohttp.ClientSession() as session,
        RatesDatabase(os.getenv("REDIS_URL")) as database,
    ):
        await proccess(session, database)


async def proccess(session: aiohttp.ClientSession, database: RatesDatabase):
    while True:
        await process_unit(session, database)
        await asyncio.sleep(60 * 60 * 24)


async def process_unit(session: aiohttp.ClientSession, database: RatesDatabase):
    text = await fetch_currency(session)
    rates = ExchangeRates.from_xml_string(text)
    await database.save(rates)


async def fetch_currency(session: aiohttp.ClientSession):
    async with session.get(CURRENCY_URL) as response:
        return await response.text(encoding="windows-1251")


if __name__ == "__main__":
    asyncio.run(main())
