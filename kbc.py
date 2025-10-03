def kbc_game():
    questions = [
        {
            "q": "What is 2 + 2?",
            "options": ["1", "2", "3", "4"],
            "ans": 4,
            "prize": 1000
        },
        {
            "q": "What is 5 * 5?",
            "options": ["10", "15", "20", "25"],
            "ans": 4,
            "prize": 2000
        }
    ]

    total = 0
    for i, ques in enumerate(questions, start=1):
        print(f"Q{i}: {ques['q']}")
        for j, opt in enumerate(ques["options"], start=1):
            print(f"({j}) {opt}")

        ans = int(input("Enter your answer (1-4): "))

        if ans == ques["ans"]:
            total += ques["prize"]
            print(f"Correct! You won ₹{ques['prize']} (Total: ₹{total})\n")
        else:
            print("Wrong answer! Game over.")
            break

    print(f"Your total winnings: ₹{total}")

kbc_game()
