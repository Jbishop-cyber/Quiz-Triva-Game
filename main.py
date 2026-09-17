import json
import random
import time
import sys
import select


def check_answers(questions):
    score = 0
    answered = 0
    time_limit = 15

    for number, item in enumerate(questions, 1):
        print(f"\nQuestion {number}: \n{item['question']}")

        for option in item["options"]:
            print(option)

        start_time = time.time()
        last_remaining = -1  # Tracks changes in seconds to reduce flickering

        while True:
            elapsed_time = time.time() - start_time
            remaining_time = max(0, int(time_limit - elapsed_time))

            # Update the visual countdown timer only when the second changes
            if remaining_time != last_remaining:
                # \r resets the cursor to the start of the row to
                # overwrite the line
                # \033[K clears everything to the right of the cursor
                print(
                    "\r⏰ ["
                    f"{remaining_time}s left] "
                    "Choose an option "
                    "(a, b, c, d or q to Quit): \033[K",
                    end="",
                    flush=True,
                )
                last_remaining = remaining_time

            if remaining_time <= 0:
                print("\n\n⏰ Time's up!\n")
                break

            # Check for keyboard input without blocking the code execution
            ready, _, _ = select.select([sys.stdin], [], [], 0.1)

            if ready:
                choice = sys.stdin.readline().strip().upper()

                if choice in ["Q", "QUIT"]:
                    print(
                        "\nExiting the game early...."
                        "Calculating your final score!"
                    )
                    return score, answered

                if choice not in ["A", "B", "C", "D"]:
                    print("\n❌ Invalid input. Please choose A, B, C, or D.")
                    # Reset last_remaining so the prompt redraws immediately
                    last_remaining = -1
                    continue

                answered += 1

                if choice == item["answer"]:
                    print("✅ Correct!\n")
                    score += 1
                else:
                    print(
                        f"❌ Wrong! The correct option was "
                        f"{item['answer']}\n"
                    )

                break

    return score, answered


def display_final_score(score, answered, total_questions):
    if answered == 0:
        print("\n😔 You didn't answer any questions.\n")
        return

    percentage = (score / answered) * 100

    if answered < total_questions:
        print(f"🤔 You answered {answered}/{total_questions} questions.")
    else:
        print("\n😄 Quiz Complete!\n")

    print(f"Your score: {score}/{answered}")
    print(f"Percentage: {percentage:.1f}%\n")

    if percentage == 100:
        print("💯 Perfect! You are a true Python master!\n")
    elif percentage >= 70:
        print("👍 Good, you know your stuff!\n")
    else:
        print("🚶🏻 Keep Practicing!\n")


def load_json():
    try:
        with open("questions.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("questions.json file not found or corrupted!")
        return []


def main():
    questions = load_json()

    if not questions:
        print("No questions available. Exiting.")
        return

    line = "-" * 25
    title = "WELCOME TO PYTHON TRIVIAS"

    print(line)
    print(title)
    print(line)

    random.shuffle(questions)

    score, answered = check_answers(questions)
    total_questions = len(questions)

    display_final_score(score, answered, total_questions)


main()
