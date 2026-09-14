import json
import random


def check_answers(questions):
    score = 0
    answered = 0

    for number, item in enumerate(questions, 1):
        print(f"Question {number}: {item['question']}")
        for option in item['options']:
            print(option)

        while True:
            # Check user input
            prompt = "Choose an option (a, b, c, d or q to Quit): "
            choice = input(prompt).strip().upper()

            if choice in ["Q", "QUIT"]:
                print(
                    "\nExiting the game early....Calculating your final "
                    "score!"
                )
                return score, answered

            if choice in ["A", "B", "C", "D"]:
                break
            print("Invalid input. Please Choose A, B, C, or D.")

        # Check the answer
        answered += 1
        if choice == item['answer']:
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong! The correct answer was {item['answer']}")

    return score, answered


def display_final_score(score, answered, total_questions):
    if answered == 0:
        print("\nYou didn't answer any questions.\n")
        return

    percentage = (score / answered) * 100

    if answered < total_questions:
        print("\nQuiz Exited Early!\n")
        print(f"You answered {answered}/{total_questions} questions.")
    else:
        print("\nQuiz Complete!\n")

    print(f"Your score: {score}/{answered}")
    print(f"Percentage: {percentage:.1f}%\n")

    if percentage == 100:
        print("Perfect! You are a true Python master!\n")
    elif percentage >= 70:
        print("Good, you know your stuff!\n")
    else:
        print("Keep Practicing!\n")


def load_json():
    try:
        with open("questions.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("questions.json file not found or corrupted!")
        return []


def main():
    line = "=" * 25
    title = "WELCOME TO PYTHON TRIVIAS"

    print(line)
    print(title)
    print(line)

    questions = load_json()
    if not questions:
        print("No questions available. Exiting.")
        return

    random.shuffle(questions)

    score, answered = check_answers(questions)
    total_questions = len(questions)

    display_final_score(score, answered, total_questions)


main()
