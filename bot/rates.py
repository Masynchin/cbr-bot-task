from fractions import Fraction
from typing import NamedTuple


class CurrencyRate(NamedTuple):
    char_code: str
    value_per_unit: Fraction

    @classmethod
    def from_bytes(cls, char_code: str, value_per_unit: bytes):
        return cls(char_code=char_code, value_per_unit=Fraction(value_per_unit.decode()))

    def exchange_to(self, other: "CurrencyRate") -> Fraction:
        return self.value_per_unit / other.value_per_unit
