import json
import os
import tempfile
from pathlib import Path

from quiz import Quiz

STATE_FILE = Path(__file__).resolve().parent / "state.json"


class QuizGame:
    def __init__(self, state_file=None):
        self.state_file = Path(state_file) if state_file is not None else STATE_FILE
        self.quizzes = []
        self.best_score = 0
        self.invalid_entries = []
        self.load_failed = False

    def add_quiz(self, question, answer, choices=None):
        self.quizzes.append(Quiz(question, answer, choices))

    def list_quizzes(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"{index}. 문제: {quiz.question}")
            if quiz.choices:
                for number, choice in enumerate(quiz.choices, start=1):
                    print(f"   {number}. {choice}")
            print(f"   정답: {quiz.answer}")

    def play_quiz(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return False

        score = 0
        for quiz in self.quizzes:
            print(f"\n문제: {quiz.question}")
            if quiz.choices:
                for number, choice in enumerate(quiz.choices, start=1):
                    print(f"{number}. {choice}")
                while True:
                    user_answer = input("정답 번호를 입력하세요 (1~4): ").strip()
                    if user_answer in ("1", "2", "3", "4"):
                        break
                    print("1~4 사이의 번호를 입력해 주세요.")
            else:
                user_answer = input("정답을 입력하세요: ")
                if not user_answer.strip():
                    print("빈 답변은 오답 처리됩니다.")
            if quiz.check_answer(user_answer):
                score += 1
                print("정답입니다!")
            else:
                print("오답입니다!")

        print(f"\n최종 점수: {score}/{len(self.quizzes)}")
        if score > self.best_score:
            self.best_score = score
            print("최고 점수가 갱신되었습니다.")
        return True

    def save_state(self):
        if self.load_failed:
            raise ValueError("읽을 수 없는 기존 state.json을 보호하기 위해 저장하지 않았습니다.")

        data = {
            "best_score": self.best_score,
            "quizzes": []
        }
        for quiz in self.quizzes:
            item = {"question": quiz.question, "answer": quiz.answer}
            if quiz.choices is not None:
                item["choices"] = quiz.choices
            data["quizzes"].append(item)
        # 기존 데이터 중 유효하지 않은 항목도 삭제하지 않고 그대로 보존합니다.
        data["quizzes"].extend(self.invalid_entries)

        temporary_name = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", delete=False,
                dir=self.state_file.parent, prefix=".state-", suffix=".tmp"
            ) as file:
                temporary_name = file.name
                json.dump(data, file, ensure_ascii=False, indent=4)
                file.write("\n")
            os.replace(temporary_name, self.state_file)
        finally:
            if temporary_name and os.path.exists(temporary_name):
                os.unlink(temporary_name)

    def load_state(self):
        try:
            with self.state_file.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            print("저장 파일이 없어 새 게임을 시작합니다.")
            return
        except (json.JSONDecodeError, UnicodeError, OSError) as error:
            self.load_failed = True
            print(f"저장 파일을 읽지 못했습니다: {error}")
            print("원본 파일을 보호하기 위해 이번 실행에서는 저장하지 않습니다.")
            return

        if (not isinstance(data, dict)
                or type(data.get("best_score")) is not int
                or data["best_score"] < 0
                or not isinstance(data.get("quizzes"), list)):
            self.load_failed = True
            print("JSON 데이터 구조가 올바르지 않아 원본을 보호합니다.")
            return

        valid_quizzes = []
        invalid_entries = []
        for entry in data["quizzes"]:
            try:
                if not isinstance(entry, dict):
                    raise ValueError("문제 형식 오류")
                valid_quizzes.append(Quiz(
                    entry["question"], entry["answer"], entry.get("choices")
                ))
            except (KeyError, TypeError, ValueError):
                invalid_entries.append(entry)

        self.best_score = data["best_score"]
        self.quizzes = valid_quizzes
        self.invalid_entries = invalid_entries
        if invalid_entries:
            print(f"주의: 유효하지 않은 문제 {len(invalid_entries)}개는 출제하지 않으며 저장 시 원본대로 보존합니다.")
