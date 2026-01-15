# LogsAnalyzer

## Пример использования

```python

# Создаем объект анализатора (по умолчанию читает "access.log")
logs_analyzer = LogsAnalyzer()

# Получаем полный анализ
print(logs_analyzer.get_full_analyze())
