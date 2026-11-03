from quiz_game import QuizGame


def main():
    game = QuizGame()
    game.load_state()

    print("코디세이 파이썬 기초 퀴즈 게임")
    print("============================")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록 보기")
    print("4. 최고 점수 보기")
    print("5. 종료")
    choice = input("메뉴 번호를 선택하세요 (1~5): ")
    if choice == "1": 
        game.play_quiz()
    elif choice == "2":
        question = input("새 퀴즈 문제를 입력하세요: ")
        answer = input("새 퀴즈 정답을 입력하세요: ")
        game.add_quiz(question, answer)
        game.save_state()
    elif choice == "3":
        game.list_quizzes()
    elif choice == "4":
        print(f"최고 점수: {game.best_score}")
    elif choice == "5":
        print("게임을 종료합니다.")
    else:
        print("잘못된 메뉴 번호입니다.")


if __name__ == "__main__":
    main()
  