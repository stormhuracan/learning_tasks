# Этот класс используется для информации о должнике
class DebtorInfo:
    def __init__(self, name, phone):
        self.name = name.strip().title()
        self.phone = phone


    # Переводит в словарь
    def to_dict(self):
        return {"name": self.name,
                "phone": self.phone}


    # Создает объект экземпляра из словаря
    @classmethod
    def from_dict(cls, data: dict) -> "DebtorInfo":
        return cls(**data)


    # Добавил возможность сравнивать должников, необходимо для проверки кто будет возвращать книгу
    def __eq__(self, other):
        if not isinstance(other, DebtorInfo):
            return NotImplemented
        return self.name == other.name and self.phone == other.phone