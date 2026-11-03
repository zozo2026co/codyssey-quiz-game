from quiz import Quiz


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = 0


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