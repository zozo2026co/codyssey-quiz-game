import json
from quiz import Quiz

STATE_FILE = "state.json"



class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = 0

    def add_quiz(self, question, answer):
        quiz = Quiz(question, answer)
        self.quizzes.append(quiz)

    def list_quizzes(self):
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"{index}. 문제: {quiz.question}")
            print(f"   정답: {quiz.answer}")

    def play_quiz(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        score = 0

        for quiz in self.quizzes:
            print(quiz.question) 

            user_answer = input("정답을 입력하세요: ")
            if quiz.check_answer(user_answer): 
                score += 1
                print("정답입니다!")
            else: 
                print("오답입니다!")

        print(f"최종 점수: {score}/{len(self.quizzes)}")

        if score > self.best_score:
            self.best_score = score 
            
    def save_state(self):
        data = {}
        data["best_score"] = self.best_score
        data["quizzes"] = []

        for quiz in self.quizzes:
            data["quizzes"].append({
                "question": quiz.question,
                "answer": quiz.answer
            })

        with open(STATE_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def load_state(self):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            print("저장된 퀴즈 파일이 없습니다. 새 게임을 시작합니다.")
            return
        except json.JSONDecodeError:
            print("저장된 JSON 파일이 손상되었습니다. 새 게임을 시작합니다.")
            return
        
        self.best_score = data["best_score"]
        self.quizzes = []

        for item in data["quizzes"]:
            quiz = Quiz(item["question"], item["answer"])
            self.quizzes.append(quiz)