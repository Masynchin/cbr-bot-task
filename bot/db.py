from redis.asyncio import Redis

from const import VALID_CURRENCIES
from rates import CurrencyRate


class RatesDatabase:
    def __init__(self, redis_url: str):
        self.client = Redis.from_url(redis_url)

    async def initialize(self):
        await self.client.initialize()

    async def exchange(self, currency_from: str, currency_to: str) -> tuple[CurrencyRate, CurrencyRate]:
        (value_per_unit_from, value_per_unit_to) = await self.client.mget((currency_from, currency_to))
        return (
            CurrencyRate.from_bytes(currency_from, value_per_unit_from),
            CurrencyRate.from_bytes(currency_to, value_per_unit_to),
        )

    async def rates(self):
        rates = await self.client.mget(VALID_CURRENCIES)
        rates = list(map(CurrencyRate.from_bytes, VALID_CURRENCIES, rates))
        return rates
