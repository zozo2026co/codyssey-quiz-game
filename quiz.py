class Quiz:
    """한 문제와 정답을 관리합니다. 기존 주관식 데이터도 읽을 수 있습니다."""

    def __init__(self, question, answer, choices=None):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제를 입력해 주세요.")
        if not isinstance(answer, str) or not answer.strip():
            raise ValueError("정답을 입력해 주세요.")
        if choices is not None:
            if (not isinstance(choices, list) or len(choices) != 4
                    or any(not isinstance(x, str) or not x.strip() for x in choices)):
                raise ValueError("보기는 내용이 있는 문자열 4개여야 합니다.")
            if answer not in ("1", "2", "3", "4"):
                raise ValueError("4지선다 정답은 1~4 중 하나여야 합니다.")
        self.question = question.strip()
        self.answer = answer.strip()
        self.choices = choices[:] if choices is not None else None

    def check_answer(self, user_answer):
        if self.choices is not None:
            return user_answer.strip() == self.answer
        return user_answer.strip().casefold() == self.answer.casefold()
