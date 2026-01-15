import re
from collections import Counter


LOG_PATTERN = re.compile(
    r'(?P<ip>\S+)\s+-\s+-\s+'
    r'\[(?P<time>[^\]]+)\]\s+'
    r'"(?P<method>\S+)\s+(?P<path>\S+)\s+[^"]+"\s+'
    r'(?P<status>\d{3})\s+(?P<size>\d+)\s+'
    r'"(?P<ua>[^"]+)"\s+'
    r'(?P<response_time>\d+\.\d+)'
)


# возвращает сырые логи
def get_logs_from_file(filepath: str) -> list:
    with open(filepath, "r", encoding='utf-8') as file:
        content = file.readlines()
        return content


# приводит к удобному виду для дальнейшего анализа
def parse_log(line: str) -> dict | None:
    match = LOG_PATTERN.match(line)
    if not match:
        return None
    return match.groupdict()


class LogsAnalyzer:
    def __init__(self, filepath: str = "access.log"):
        self.filepath = filepath
        self.logs = [log for log in (parse_log(line) for line in get_logs_from_file(self.filepath))
                     if log is not None] # парсим логи и проверяем, чтобы не было None
        if not self.logs:
            raise ValueError("В файле нет логов, удовлетворяющих паттерну поиска!")

    # Считает пост и гет запросы
    def calculate_method_requests(self) -> dict:
        return dict(Counter(log['method'] for log in self.logs))


    # Срднее время ответа
    def avg_response_time(self) -> float:
        return round(sum(float(rt['response_time']) for rt in self.logs) / len(self.logs), 3)


    # Считает кол-во айпишников, по дефолту отдает максимум 10 айпи
    def get_top_ips(self, limit=10) -> dict:
        return dict(sorted(Counter(log['ip'] for log in self.logs).items(), key=lambda x: x[1], reverse=True)[:limit])


    # Находит самый частый user-agent
    def most_common_ua(self) -> dict:
        return dict(Counter(ua['ua'] for ua in self.logs).most_common(1))


    # Считает все коды, есть параметр, какие коды ловить
    def calculate_status_codes(self, between: tuple[int, int] = (0, 600)) -> dict:
        return dict(sorted(Counter(s['status'] for s in self.logs \
                                   if between[0] <= int(s['status']) <= between[1]).items(),
                           key=lambda x: x[1], reverse=True))


    # Считает ошибки 400-500 кодов.
    def calculate_errors(self, ) -> dict:
        return self.calculate_status_codes(between=(400, 600))

    # Полный анализ логов
    def get_full_analyze(self) -> str:
        return (f'Количество запросов по методам: {self.calculate_method_requests()}\n'
                f'Среднее время ответа: {self.avg_response_time()} сек.\n'
                f'Топ 10 IP адресов: {self.get_top_ips()}\n'
                f'Самый частый User-Agent: {self.most_common_ua()}\n'
                f'Ошибки: {self.calculate_errors()}')
