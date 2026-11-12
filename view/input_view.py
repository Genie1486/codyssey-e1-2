from constants.error_message import ErrorMessage


class InputView:
    CHOICE = "선택: "
    QUESTION = "문제를 입력하세요: "
    CHOICE_I = "선택지 {}: "
    ANSWER = "정답번호 (1-4): "
    HINT = "힌트 (선택사항, 엔터 입력 시 등록 안 함): "
    INPUT_ANSWER = "정답 입력: "
    QUIZ_COUNT = "몇 문제를 푸시겠습니까? ({min_val}~{max_val} 숫자 입력): "

    @classmethod
    def get_number_in_range(cls, prompt: str, min_val: int, max_val: int) -> int:
        """범위 내의 정수를 입력받음"""
        return cls._get_user_number_until_valid(prompt, min_val, max_val)

    @classmethod
    def get_quiz_answer(cls, min_val: int, max_val: int) -> int:
        """퀴즈 답변 입력"""
        return cls.get_number_in_range(cls.INPUT_ANSWER, min_val, max_val)

    @classmethod
    def get_menu_choice(cls, min_val: int, max_val: int) -> int:
        """메뉴 선택 입력"""
        return cls.get_number_in_range(cls.CHOICE, min_val, max_val)

    @classmethod
    def get_quiz_count(cls, min_val: int, max_val: int) -> int:
        """문제 수 입력"""
        return cls.get_number_in_range(
            cls.QUIZ_COUNT.format(min_val=min_val, max_val=max_val), min_val, max_val
        )

    @classmethod
    def get_quiz_input(cls):
        """새로운 퀴즈 입력받기"""
        quiz_dict = {}

        # 문제 입력
        quiz_dict["question"] = cls._get_user_input_until_valid(cls.QUESTION)

        # 선택지 4개 입력
        choices = []
        for i in range(1, 5):
            choice = cls._get_user_input_until_valid(cls.CHOICE_I.format(i))
            choices.append(choice)
        quiz_dict["choices"] = choices

        # 정답 입력
        quiz_dict["answer"] = cls._get_user_number_until_valid(cls.ANSWER, 1, 4)

        # 🆕 힌트 입력 (선택사항, 한 번만)
        quiz_dict["hint"] = input(cls.HINT).strip()

        print(quiz_dict)

        return quiz_dict

    # ============ 헬퍼 메서드 ============

    @classmethod
    def _get_user_input_until_valid(cls, prompt: str) -> str:
        """텍스트 입력을 반복해서 받기"""
        while True:
            user_input = input(prompt)
            validated = cls._validate_text_input(user_input)
            if validated is not None:
                return validated

    @classmethod
    def _get_user_number_until_valid(
        cls, prompt: str, min_val: int, max_val: int
    ) -> int:
        """정수 입력을 반복해서 받기"""
        while True:
            user_input = input(prompt)
            validated = cls._validate_integer_input(user_input, min_val, max_val)
            if validated is not None:
                return validated

    @classmethod
    def _validate_integer_input(
        cls, user_input: str, min_val: int, max_val: int
    ) -> int | None:
        """정수 입력 검증"""
        validated_number = user_input.strip()

        # 빈값 검증
        if len(validated_number) == 0:
            print(
                f"{ErrorMessage.EMPTY_INPUT.value} {ErrorMessage.NUMBER_RANGE.value.format(min_val,max_val)}"
            )
            return None

        # 정수 변환 검증
        try:
            validated_number = int(validated_number)
        except ValueError:
            print(
                f"{ErrorMessage.NOT_AN_INTEGER.value} {ErrorMessage.NUMBER_RANGE.value.format(min_val,max_val)}"
            )
            return None

        # 범위 검증 (동적 메시지!)
        if not (min_val <= validated_number <= max_val):
            print(
                f"{ErrorMessage.OUT_OF_RANGE.value} {ErrorMessage.NUMBER_RANGE.value.format(min_val,max_val)}"
            )
            return None

        return validated_number

    @classmethod
    def _validate_text_input(cls, user_input: str) -> str | None:
        """필수 텍스트 검증"""
        validated_text = user_input.strip()

        if len(validated_text) == 0:
            print(ErrorMessage.EMPTY_INPUT.value)
            return None

        return validated_text
