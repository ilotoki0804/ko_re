from typing import Literal

def compilestr(
    pattern: str,
    order: Literal["default", "regular_first"] | None = "default",
) -> str:
    """kre용 정규 표현식을 일반적으로 사용할 수 있는 정규 표현식으로 컴파일합니다."""
