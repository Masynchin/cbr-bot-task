"""Схема данных домена.

Актуальность XML-схемы курса ЦБ РФ: 2024.07.22
"""

import datetime as dt
from fractions import Fraction
from typing import NamedTuple
from xml.etree import ElementTree


class ExchangeRate(NamedTuple):
    """Курс конкретной валюты к рублю.

    `char_code` - ISO Символьный код валюты.
    `value_per_unit` - Курс за 1 единицу валюты.
    """

    char_code: str
    value_per_unit: Fraction

    @classmethod
    def from_xml(cls, xml: ElementTree):
        """Из XML элемента.

        Как выглядит XML:

        ~~~xml
        <Valute ID="R01090B">
            <NumCode>933</NumCode>
            <CharCode>BYN</CharCode>
            <Nominal>1</Nominal>
            <Name>Белорусский рубль</Name>
            <Value>27,7580</Value>
            <VunitRate>27,758</VunitRate>
        </Valute>
        ~~~
        """
        char_code = xml.find("CharCode").text
        value_per_unit = Fraction(
            xml.find("VunitRate").text.replace(",", ".", 1)
        )
        return cls(char_code=char_code, value_per_unit=value_per_unit)


class ExchangeRates(NamedTuple):
    """Курс валют к рублю.

    `date` - актуальность курса.
    `rates` - курсы конкретных валют к рублю.
    """

    date: dt.date
    rates: tuple[ExchangeRate, ...]

    @classmethod
    def from_xml(cls, xml: ElementTree):
        """Из XML элемента.

        Как выглядит XML:

        ~~~xml
        <ValCurs Date="20.07.2024" name="Foreign Currency Market">
            <Valute ID="R01090B">...</Valute>
            ...
        </ValCurs>
        ~~~
        """
        date = dt.datetime.strptime(xml.attrib["Date"], "%d.%m.%Y").date()
        rates = tuple(ExchangeRate.from_xml(rate) for rate in xml)
        return cls(date=date, rates=rates)

    @classmethod
    def from_xml_string(cls, xml: str):
        """Из строки с XML данными."""
        return cls.from_xml(ElementTree.fromstring(xml))

    def add(self, rate: ExchangeRate):
        """Добавление другого курса валюты."""
        return self._replace(rates=(*self.rates, rate))
