import pytest
import csv
import yaml

from main import CurrenciesCBR, ConvertToYAML, ConvertToCSV

CBR_DAILY_URL = "https://www.cbr-xml-daily.ru/daily_json.js"

MOCK_SUCCESS_RESPONSE = {
    "Date": "2026-03-24T11:30:00+03:00",
    "Valute": {
        "BYN": {
            "ID": "R01090B",
            "NumCode": "933",
            "CharCode": "BYN",
            "Nominal": 1,
            "Name": "Белорусский рубль",
            "Value": 27.5076,
            "Previous": 27.9175
        },
        "CNY": {
            "ID": "R01375",
            "NumCode": "156",
            "CharCode": "CNY",
            "Nominal": 1,
            "Name": "Юань",
            "Value": 11.8709,
            "Previous": 12.2171
        }
    }
}

MOCK_FAILURE_RESPONSE = {
    "Date": "2026-03-24T11:30:00+03:00"
}


# ============================================================================
# Тесты для базового класса: CurrenciesCBR
# ============================================================================

def test_currencies_cbr_success(requests_mock):
    """SUCCESS: Проверка успешного получения данных о валютах."""

    requests_mock.get(CBR_DAILY_URL, json=MOCK_SUCCESS_RESPONSE, status_code=200)

    obj = CurrenciesCBR()
    data = obj.get_currencies()

    assert isinstance(data, dict)
    assert "BYN" in data
    assert "CNY" in data
    assert data["BYN"]["ID"] == "R01090B"
    assert data["CNY"]["NumCode"] == "156"

def test_currencies_cbr_failure(requests_mock):
    """FAILURE: Проверка обработки ответа без ключа 'Valute'."""

    requests_mock.get(CBR_DAILY_URL, json=MOCK_FAILURE_RESPONSE, status_code=200)

    obj = CurrenciesCBR()
    with pytest.raises(KeyError, match="Valute"):
        obj.get_currencies()


# ============================================================================
# Тесты для декоратора CSV: ConvertToCSV
# ============================================================================

def test_get_currencies_csv_format(requests_mock):
    """SUCCESS: Проверка формата данных после CSV-декоратора."""

    requests_mock.get(CBR_DAILY_URL, json=MOCK_SUCCESS_RESPONSE, status_code=200)

    obj = ConvertToCSV(CurrenciesCBR())
    data = obj.get_currencies_csv()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["val_id"] in ["BYN", "CNY"]
    assert "CharCode" in data[0]
    assert "Value" in data[0]

def test_csv_save_to_file(requests_mock, tmp_path):
    """SUCCESS: Проверка записи корректного CSV-файла."""

    requests_mock.get(CBR_DAILY_URL, json=MOCK_SUCCESS_RESPONSE, status_code=200)
    test_file = tmp_path / "test.csv"

    obj = ConvertToCSV(CurrenciesCBR())
    obj.save_to_file(filepath = str(test_file))

    with open(test_file, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

        assert reader.fieldnames is not None
        assert "val_id" in reader.fieldnames
        assert len(rows) == 2

        byn_row = next((r for r in rows if r["val_id"] == "BYN"), None)
        assert byn_row is not None
        assert byn_row["Value"] == "27.5076"


# ============================================================================
# Тесты для декоратора YAML: ConvertToYAML
# ============================================================================

def test_get_currencies_yaml_format(requests_mock):
    """SUCCESS: Проверка, что YAML-декоратор возвращает корректные данные."""

    requests_mock.get(CBR_DAILY_URL, json=MOCK_SUCCESS_RESPONSE, status_code=200)

    obj = ConvertToYAML(CurrenciesCBR())
    data = obj.get_currencies()

    assert isinstance(data, dict)
    assert "CNY" in data
    assert data["CNY"]["Name"] == "Юань"
    assert data["BYN"]["NumCode"] == "933"

def test_yaml_save_to_file(requests_mock, tmp_path):
    """SUCCESS: Проверка записи валидного YAML-файла."""

    requests_mock.get(CBR_DAILY_URL, json=MOCK_SUCCESS_RESPONSE, status_code=200)
    test_file = tmp_path / "test.yaml"

    obj = ConvertToYAML(CurrenciesCBR())
    obj.save_to_file(filepath = str(test_file))

    with open(test_file, "r", encoding="utf-8") as file:
        content = file.read()

        assert "BYN:" in content
        assert "Белорусский рубль" in content
        assert "Nominal: 1" in content

        parsed = yaml.safe_load(content)
        assert parsed["BYN"]["CharCode"] == "BYN"

