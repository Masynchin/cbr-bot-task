from redis.asyncio import Redis

from schema import ExchangeRates


class RatesDatabase:
    def __init__(self, redis_url: str):
        self.client = Redis.from_url(redis_url)

    async def __aenter__(self):
        await self.client.initialize()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.aclose()

    async def save(self, rates: ExchangeRates):
        pipe = self.client.pipeline()
        for rate in rates.rates:
            pipe.set(rate.char_code, str(rate.value_per_unit))
        await pipe.execute()
