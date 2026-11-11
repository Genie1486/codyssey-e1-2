from constants.error_message import ErrorMessage


class InputView:
    CHOICE = "선택: "

    @classmethod
    def get_menu_choice(cls, min_val: int, max_val: int) -> int:
        while True:
            user_input = input(cls.CHOICE).strip()

            validated = cls._validate_integer_input(user_input, min_val, max_val)
            if validated is not None:
                return validated

    @classmethod
    def _validate_integer_input(
        cls, user_input: str, min_val: int, max_val: int
    ) -> int | None:
        # 빈값 검증
        if len(user_input) == 0:
            print(ErrorMessage.EMPTY_INPUT.value.format(min_val, max_val))
            return None

        # 정수 변환 검증
        try:
            choice = int(user_input)
        except ValueError:
            print(ErrorMessage.INVALID_TYPE.value.format(min_val, max_val))
            return None

        # 범위 검증 (동적 메시지!)
        if not (min_val <= choice <= max_val):
            print(ErrorMessage.OUT_OF_RANGE.value.format(min_val, max_val))
            return None

        return choice

    @classmethod
    def _validate_text_input(cls, user_input: str) -> str | None:
        # 빈값 검증
        if len(user_input) == 0:
            print(ErrorMessage.EMPTY_INPUT.value)
            return None

        return user_input
