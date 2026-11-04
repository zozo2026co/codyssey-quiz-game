
from quiz_game import QuizGame


def read_menu():
    while True:
        choice = input("메뉴 번호를 선택하세요 (1~5): ").strip()
        if choice in ("1", "2", "3", "4", "5"):
            return choice
        print("잘못된 메뉴 번호입니다. 1~5 사이의 숫자를 입력해 주세요.")


def add_new_quiz(game):
    question = input("새 퀴즈 문제를 입력하세요: ").strip()
    if not question:
        print("문제를 비워 둘 수 없습니다.")
        return

    choices = []
    for number in range(1, 5):
        choice = input(f"보기 {number}: ").strip()
        if not choice:
            print("보기를 비워 둘 수 없습니다. 문제 추가를 취소합니다.")
            return
        choices.append(choice)

    while True:
        answer = input("정답 번호 (1~4): ").strip()
        if answer in ("1", "2", "3", "4"):
            break
        print("정답 번호는 1~4 중 하나여야 합니다.")

    game.add_quiz(question, answer, choices)
    try:
        game.save_state()
        print("퀴즈가 추가되고 저장되었습니다.")
    except (OSError, ValueError) as error:
        print(f"퀴즈는 현재 실행에만 추가되었습니다. 저장 실패: {error}")


def main():
    game = QuizGame()
    game.load_state()

    print("코디세이 파이썬 기초 퀴즈 게임")
    while True:
        print("\n============================")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록 보기")
        print("4. 최고 점수 보기")
        print("5. 종료")

        try:
            choice = read_menu()
            if choice == "1":
                if game.play_quiz():
                    try:
                        game.save_state()
                    except (OSError, ValueError) as error:
                        print(f"최고 점수를 저장하지 못했습니다: {error}")
            elif choice == "2":
                add_new_quiz(game)
            elif choice == "3":
                game.list_quizzes()
            elif choice == "4":
                print(f"최고 점수: {game.best_score}/{len(game.quizzes)}")
            else:
                print("게임을 종료합니다.")
                break
        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되어 게임을 안전하게 종료합니다.")
            break


if __name__ == "__main__":
    main()
