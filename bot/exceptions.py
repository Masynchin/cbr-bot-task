class NoArgumentsPassed(Exception):
    """Не переданы аргументы в команду `/exchange`"""


class WrongArgumentCount(Exception):
    """Неверное количество аргументов команды `exchange`"""


class InvalidAmount(Exception):
    """Неправильно указано число валюты в команде `/exchange`"""


class InvalidCurrency(Exception):
    """Неизвестные валюты переданы в команду `/exchange`"""
