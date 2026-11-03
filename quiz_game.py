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