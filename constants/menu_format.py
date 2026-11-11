from enum import Enum


class MenuFormat(Enum):
    PADDING = "        "  # 가운데 정렬용 공백
    SEPARATOR = " | "
    DIVIDER = "=" * 40
    NEWLINE = ""  # 한 줄 띄우기
