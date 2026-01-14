class Counter:
    def __init__(self, text: str):
        self.text = text

    # инкапсулируемая логика анализа
    def analyze(self) -> dict[str, int]:
        letters = digits = spaces = 0
        for char in self.text:
            if char.isalpha():
                letters += 1
            elif char.isdigit():
                digits += 1
            elif char == " ":
                spaces += 1

        return {"letters": letters,
                "digits": digits,
                "spaces": spaces
                }

    # Красивый вывод анализа
    def pretty_analyze(self) -> str:
        analyze = self.analyze()
        result_text = (f'Количество букв в тексте: {analyze["letters"]}\n'
                       f'Количество цифр в тексте: {analyze["digits"]}\n'
                       f'Количество пробелов в тексте: {analyze["spaces"]}\n')
        return result_text
