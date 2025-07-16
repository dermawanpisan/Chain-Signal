"""
Silent Gas Auditor — анализатор скрытых и неожиданных трат газа в смарт-контрактных взаимодействиях.

Получает историю транзакций адреса и ищет аномалии в потреблении газа:
- неожиданные пики (возможно атака или неэффективный контракт)
- дорогостоящие внутренние вызовы
- попытки frontrun или MEV
"""

import requests
import argparse
import statistics


ETHERSCAN_API_URL = "https://api.etherscan.io/api"


def fetch_transactions(address, api_key):
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": api_key
    }
    response = requests.get(ETHERSCAN_API_URL, params=params)
    result = response.json()
    return result.get("result", [])


def analyze_gas_usage(transactions):
    gas_usages = [int(tx["gasUsed"]) for tx in transactions if tx["isError"] == "0"]
    if len(gas_usages) < 5:
        print("Недостаточно данных для анализа.")
        return []

    median = statistics.median(gas_usages)
    stddev = statistics.stdev(gas_usages)

    anomalies = []
    for tx in transactions:
        if tx["isError"] == "1":
            continue
        gas = int(tx["gasUsed"])
        if gas > median + 2 * stddev:
            anomalies.append({
                "hash": tx["hash"],
                "gasUsed": gas,
                "to": tx["to"],
                "value": int(tx["value"]) / 1e18,
                "input": tx["input"][:10]
            })

    return anomalies


def main(address, api_key):
    print(f"[•] Анализируем адрес: {address}")
    txs = fetch_transactions(address, api_key)
    print(f"[✓] Загружено {len(txs)} транзакций.")
    anomalies = analyze_gas_usage(txs)

    print("\n[!] Подозрительные транзакции по расходу газа:")
    if not anomalies:
        print("  — Не обнаружено.")
    else:
        for tx in anomalies:
            print(f"  - TX {tx['hash']} → {tx['gasUsed']} газа, {tx['value']} ETH, метод {tx['input']}, to {tx['to']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Silent Gas Auditor — поиск аномального потребления газа")
    parser.add_argument("address", help="Ethereum-адрес для анализа")
    parser.add_argument("api_key", help="API-ключ от Etherscan")
    args = parser.parse_args()

    main(args.address, args.api_key)
