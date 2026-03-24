import requests
import json
import csv
import yaml
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List

CBR_DAILY_URL = "https://www.cbr-xml-daily.ru/daily_json.js"


class Currencies(ABC):
    """Абстрактный компонент: базовый интерфейс для получения данных."""

    @abstractmethod
    def get_currencies(self) -> Dict[str, Any]:
        """Получить данные о валютах в виде словаря."""
        pass

    @abstractmethod
    def save_to_file(self, filepath: str) -> None:
        """Сохранить данные в файл."""
        pass

class CurrenciesCBR(Currencies):
    """Конкретный компонент: получение данных с API ЦБ РФ."""

    def __init__(self, url: str = CBR_DAILY_URL):
        self._url = url
        self._data: Dict[str, Any] = {}

    def get_currencies(self) -> Dict[str, Any]:
        response = requests.get(self._url)
        response.raise_for_status()

        data = response.json()
        if "Valute" not in data:
            raise KeyError("Ключ 'Valute' отсутствует в ответе API")

        self._data = data
        return data["Valute"]

    def save_to_file(self, filepath: str = "./files/currencies.json") -> None:
        if not self._data:
            self.get_currencies()

        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(self._data, file, ensure_ascii=False, indent=4)

class CurrencyDecorator(Currencies):
    """Базовый декоратор: хранит ссылку на обёртываемый объект."""

    def __init__(self, currencies: Currencies):
        self._currencies = currencies

    def get_currencies(self) -> Dict[str, Any]:
        return self._currencies.get_currencies()

    def save_to_file(self, filepath: str) -> None:
        return self._currencies.save_to_file(filepath)

class ConvertToCSV(CurrencyDecorator):
    """Декоратор: конвертация данных в CSV-формат."""

    def get_currencies_csv(self) -> List[Dict[str, Any]]:
        """Получить данные в формате, готовом для CSV (список словарей)."""
        data = self._currencies.get_currencies()

        if not data:
            raise ValueError("Нет данных для конвертации")

        result = []
        for currency_id, currency_info in data.items():
            row = {"val_id": currency_id, **currency_info}
            result.append(row)

        return result

    def save_to_file(self, filepath: str = "./files/currencies.csv") -> None:
        rows = self.get_currencies_csv()
        if not rows:
            raise ValueError("Пустые данные")

        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        fieldnames = ["val_id"] + list(rows[0].keys())

        with open(filepath, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=",")
            writer.writeheader()
            writer.writerows(rows)

class ConvertToYAML(CurrencyDecorator):
    """Декоратор: конвертация данных в YAML-формат."""

    def get_currencies(self) -> Dict[str, Any]:
        return self._currencies.get_currencies()

    def get_currencies_yaml(self) -> str:
        """Получить данные в YAML-формате как строку."""
        data = self._currencies.get_currencies()
        return yaml.dump(data, allow_unicode=True, sort_keys=False)

    def save_to_file(self, filepath: str = "./files/currencies.yaml") -> None:
        data = self.get_currencies_yaml()

        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as file:
            file.write(data)
