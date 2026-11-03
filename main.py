
def main():
    print("코디세이 파이썬 기초 퀴즈 게임")
    print("============================")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록 보기")
    print("4. 최고 점수 보기")
    print("5. 종료")
    choice = input("메뉴 번호를 선택하세요 (1~5): ")
    if choice == "1":
        print("퀴즈 풀기 기능을 준비 중입니다.")
    elif choice == "2":
        print("퀴즈 추가 기능을 준비 중입니다.")
    elif choice == "3":
        print("퀴즈 목록 보기 기능을 준비 중입니다.")
    elif choice == "4":
        print("최고 점수 보기 기능을 준비 중입니다.")
    elif choice == "5":
        print("게임을 종료합니다.")
    else:
        print("잘못된 메뉴 번호입니다.")


if __name__ == "__main__":
    main()
  