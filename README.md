# Silent Gas Auditor

**Silent Gas Auditor** — утилита, которая сканирует историю транзакций Ethereum-адреса и выявляет **аномалии в потреблении газа**.

### Что делает:

- Определяет транзакции, в которых газ значительно превышает норму.
- Помогает обнаружить **скрытые ошибки**, **MEV-атаки**, **вредоносные вызовы**, **неоптимальные контракты**.
- Работает через API [Etherscan](https://etherscan.io/).

---

## Установка

```bash
pip install -r requirements.txt
```

## Использование

```bash
python silent_gas_auditor.py <ETH_ADDRESS> <ETHERSCAN_API_KEY>
```

### Пример:

```bash
python silent_gas_auditor.py 0xABCDEF1234567890ABCDEF1234567890ABCDEF12 YOUR_API_KEY
```

---

## Пример вывода:

```
[!] Подозрительные транзакции:
  - TX 0xabc... → 195482 газа, 0.03 ETH, метод 0xa9059cbb, to 0xdef...
  - TX 0xdef... → 202912 газа, 0.00 ETH, метод 0x095ea7b3, to 0xabc...
```

---

## Зачем это нужно?

Это инструмент для тех, кто хочет **аудировать собственные кошельки** или **мониторить чужие**, чтобы находить утечки, подозрительные взаимодействия и ошибки, которые остаются незамеченными.

## Лицензия

MIT
