import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from quiz import Quiz
from quiz_game import QuizGame
from main import add_new_quiz, main, read_menu


class QuizTests(unittest.TestCase):
    def test_multiple_choice(self):
        quiz = Quiz("함수는?", "2", ["변수", "print()", "정수", "리스트"])
        self.assertTrue(quiz.check_answer(" 2 "))
        self.assertFalse(quiz.check_answer("1"))

    def test_legacy_short_answer(self):
        self.assertTrue(Quiz("함수는?", "print()").check_answer(" PRINT() "))

    def test_invalid_multiple_choice(self):
        with self.assertRaises(ValueError):
            Quiz("함수는?", "5", ["a", "b", "c", "d"])
        with self.assertRaises(ValueError):
            Quiz("함수는?", "2", ["a", "b"])


class StateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "state.json"

    def tearDown(self):
        self.temp.cleanup()

    def test_save_and_reload(self):
        game = QuizGame(self.path)
        game.add_quiz("Python에서 출력하는 함수는?", "2", ["len()", "print()", "input()", "str()"])
        game.best_score = 1
        game.save_state()
        other = QuizGame(self.path)
        other.load_state()
        self.assertEqual(other.best_score, 1)
        self.assertEqual(len(other.quizzes), 1)
        self.assertTrue(other.quizzes[0].check_answer("2"))

    def test_missing_state(self):
        game = QuizGame(self.path)
        with contextlib.redirect_stdout(io.StringIO()):
            game.load_state()
        self.assertFalse(game.load_failed)

    def test_corrupted_json_preserved(self):
        self.path.write_text("{not json", encoding="utf-8")
        game = QuizGame(self.path)
        with contextlib.redirect_stdout(io.StringIO()):
            game.load_state()
        self.assertTrue(game.load_failed)
        with self.assertRaises(ValueError):
            game.save_state()
        self.assertEqual(self.path.read_text(encoding="utf-8"), "{not json")

    def test_invalid_structure_preserved(self):
        self.path.write_text('{"quizzes":[]}', encoding="utf-8")
        game = QuizGame(self.path)
        with contextlib.redirect_stdout(io.StringIO()):
            game.load_state()
        self.assertTrue(game.load_failed)

    def test_invalid_entry_kept_not_played(self):
        data = {"best_score": 1, "quizzes": [
            {"question": "문제?", "answer": "1", "choices": ["a", "b", "c", "d"]},
            {"question": "잘못된 문제?", "answer": ""}
        ]}
        self.path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        game = QuizGame(self.path)
        with contextlib.redirect_stdout(io.StringIO()):
            game.load_state()
        self.assertEqual(len(game.quizzes), 1)
        self.assertEqual(len(game.invalid_entries), 1)
        game.save_state()
        saved = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(saved["quizzes"][1], data["quizzes"][1])

    def test_play_updates_best(self):
        game = QuizGame(self.path)
        game.add_quiz("문제?", "1", ["a", "b", "c", "d"])
        with patch("builtins.input", side_effect=["0", "1"]):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertTrue(game.play_quiz())
        self.assertEqual(game.best_score, 1)

    def test_new_quiz_input(self):
        game = QuizGame(self.path)
        with patch("builtins.input", side_effect=["함수?", "a", "b", "c", "d", "5", "2"]):
            with contextlib.redirect_stdout(io.StringIO()):
                add_new_quiz(game)
        self.assertEqual(len(game.quizzes), 1)
        self.assertEqual(game.quizzes[0].answer, "2")
        self.assertTrue(self.path.exists())


class MenuTests(unittest.TestCase):
    def test_invalid_menu_then_exit(self):
        with patch("builtins.input", side_effect=["", "abc", "0", "5"]):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(read_menu(), "5")

    def test_eof_safe_exit(self):
        # main()이 참조하는 기본 파일은 테스트 중 임시 파일로 대체합니다.
        with tempfile.TemporaryDirectory() as folder:
            with patch("quiz_game.STATE_FILE", Path(folder) / "state.json"):
                with patch("builtins.input", side_effect=EOFError):
                    output = io.StringIO()
                    with contextlib.redirect_stdout(output):
                        main()
                    self.assertIn("안전하게 종료", output.getvalue())


if __name__ == "__main__":
    unittest.main()
