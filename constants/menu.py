from enum import Enum


class MenuInfo:
    def __init__(self, number: int, display_name: str):
        self.number = number
        self.display_name = display_name


class Menu(Enum):
    PLAY = MenuInfo(1, "퀴즈 풀기")
    ADD = MenuInfo(2, "퀴즈 추가")
    LIST = MenuInfo(3, "퀴즈 목록")
    SCORE = MenuInfo(4, "점수 확인")
    EXIT = MenuInfo(5, "종료")

    @property
    def number(self):
        return self.value.number

    @property
    def display_name(self):
        return self.value.display_name

    @classmethod
    def number_range(cls) -> tuple[int, int]:
        numbers = [m.number for m in cls]
        return min(numbers), max(numbers)
