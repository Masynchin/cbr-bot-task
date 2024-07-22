import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from const import VALID_CURRENCIES
from db import RatesDatabase
from rates import CurrencyRate
import exceptions


dp = Dispatcher()
db: RatesDatabase


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Hello and welcome!")


@dp.message(Command("rates"))
async def rates(message: Message):
    rates = await db.rates()
    text = "\n".join(f"`{rate.char_code}`: {rate.value_per_unit:.3f}" for rate in rates)
    await message.answer(f"Текущие курсы валют к рублю:\n\n{text}", parse_mode="Markdown")


@dp.message(Command("exchange"))
async def exchange(message: Message, command: CommandObject):
    try:
        (currency_from, currency_to, amount) = parse_exchange_arguments(command.args)
        (rate_from, rate_to) = await db.exchange(currency_from, currency_to)
        exchange_rate = rate_from.exchange_to(rate_to)
        exchange_amount = exchange_rate * amount
        await message.answer(
            f"{amount} {currency_from} будет стоить {exchange_amount:.3f} {currency_to}"
        )
    except exceptions.NoArgumentsPassed:
        await message.answer("Передайте аргументы, например: /exchange USD RUB 10")
    except exceptions.WrongArgumentCount:
        await message.answer("Передайте три аргумента, например: /exchange USD RUB 10")
    except exceptions.InvalidAmount:
        await message.answer("Используйте число для количества к обмену")
    except exceptions.InvalidCurrency:
        await message.answer("Не могу распознать валюту")


def parse_exchange_arguments(text: str | None) -> tuple[str, str, int]:
    if text is None:
        raise exceptions.NoArgumentsPassed

    parts = text.split(" ")
    if len(parts) != 3:
        raise exceptions.WrongArgumentCount

    (currency_from, currency_to, amount) = parts
    if not amount.isdigit():
        raise exceptions.InvalidAmount

    currency_from = currency_from.upper()
    currency_to = currency_to.upper()
    if currency_from not in VALID_CURRENCIES or currency_to not in VALID_CURRENCIES:
        raise exceptions.InvalidCurrency

    return (currency_from, currency_to, int(amount))


@dp.message()
async def unrecognized(message: Message):
    await message.answer("Не могу распознать команду")


async def main():
    global db

    bot = Bot(token=os.getenv("BOT_TOKEN"))
    db = RatesDatabase(os.getenv("REDIS_URL"))
    await db.initialize()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
