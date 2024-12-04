import csv
import os
import pyfiglet
import time
from ClearConsole import clear_console
from pathlib import Path
import sys
from colorama import init, Fore
import random

init(autoreset=True)

username = ""
log_file = "log.csv"
games = "games.csv"

RED = Fore.RED
GREEN = Fore.GREEN 
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
MAGENTA = Fore.MAGENTA
CYAN = Fore.CYAN

colors = [RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN]



def main():
    intro()
    menu()


def intro():
    global username

    if Path("log.csv").is_file():
        with open("log.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                username = row[0]
                break
        print(pyfiglet.figlet_format("Game  Journal", font="big"))
        print(f"Welcome to {username}'s Game Journal!")
    else:
        username = input("What is your name? ")
        with open("log.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([username])
        clear_console()
        print(pyfiglet.figlet_format("Game  Journal", font="big"))
        print(f"Welcome to {username}'s Game Journal!")

    time.sleep(2)
    clear_console()


def menu():
    while True:
        print(random_color() + pyfiglet.figlet_format("Game  Journal", font="big"))
        print(
            "1. View Games\n2. Add Games\n3. Remove Games\n4. Change Game Completion\n5. View Reviews\n6. Add Review\n7. Exit"
        )
        select = str(input("\n> ")).strip().lower()

        # View Games
        if select[0] == "1" or "view game" in select:
            clear_console()
            print("\n=-- Games List --=\n\n")
            try:
                with open("games.csv", "r") as file:
                    games_reader = csv.reader(file)
                    games_data = {
                        row[0].strip().lower(): row[1].strip()
                        for row in games_reader
                        if row
                    }

                    reviews = {}
                    if Path("reviews.csv").is_file():
                        with open("reviews.csv", "r") as file:
                            reviews_reader = csv.reader(file)
                            for row in reviews_reader:
                                if row:
                                    game_name = row[0].strip().lower()
                                    review_score = row[2].strip()
                                    reviews[game_name] = review_score

                    incomplete_games = {
                        name: completed
                        for name, completed in sorted(games_data.items())
                        if completed.lower() == "false"
                    }
                    completed_games = {
                        name: completed
                        for name, completed in sorted(games_data.items())
                        if completed.lower() == "true"
                    }

                    print("=-- Incomplete Games --=\n")
                    for game_name, completed in incomplete_games.items():
                        status = "Incomplete"
                        give_color = "\033[91m"
                        reset_color = "\033[0m"
                        score = reviews.get(game_name, "N/A")
                        print(
                            f"{game_name.title()} : {give_color}{status}{reset_color}"
                        )

                    print("\n\n=-- Completed Games --=\n")
                    for game_name, completed in completed_games.items():
                        status = "Completed"
                        give_color = "\033[92m"
                        reset_color = "\033[0m"
                        score = reviews.get(game_name, "N/A")
                        if score == "N/A":
                            score_display = "N/A"
                        else:
                            rounded_score = round(float(score), 1)
                            score_display = (
                                f"{int(rounded_score)}/10"
                                if rounded_score.is_integer()
                                else f"{rounded_score}/10"
                            )
                        print(
                            f"{game_name.title()} : {give_color}{status}{reset_color} (Score: {score_display})"
                        )

            except FileNotFoundError:
                print("No games found. Please add some games first!")
                time.sleep(2)
                clear_console()

            while True:
                print(
                    'Type "exit" to quit or "back" to go to menu\n------------------------------------------------------'
                )
                choice = input("> ")
                if choice == "exit":
                    print("Closing...")
                    time.sleep(1)
                    sys.exit()
                elif choice == "back":
                    clear_console()
                    break
                else:
                    print("Unknown Slection")
                    time.sleep(2)
                    clear_console()
                    continue

        # Add Games
        elif select[0] == "2" or "add game" in select:
            clear_console()
            print("\n=-- Add Games --=\n\n")
            num_order = 1
            games = []
            print(
                'Enter name of game. Type "exit" to quit or "back" to go to menu\n-----------------------------'
            )
            while True:
                game_name = input(f"{num_order}. ").strip().lower()
                if game_name == "exit":
                    print("Closing...")
                    time.sleep(1)
                    sys.exit()
                elif game_name == "back":
                    clear_console()
                    break
                while True:
                    completed = input("Have you beat the game? ").strip().lower()
                    if completed not in ["yes", "no", "y", "n"]:
                        print("Please answer with yes or no\n")
                        continue
                    else:
                        break

                completed_status = "True" if completed in ["yes", "y"] else "False"

                with open("games.csv", "a") as file:
                    writer = csv.writer(file)
                    writer.writerow([game_name, completed_status])

                print(f"{game_name.title()} has been added to your Game List\n")
                num_order += 1
                continue

        # Remove Games
        elif select[0] == "3" or "remove game" in select:
            clear_console()
            print("\n=-- Remove Games --=\n\n")
            print(
                'Enter name of game. Type "exit" to quit or "back" to go to menu\n-----------------------------'
            )
            game_name_remove = input("> ").strip().lower()

            if game_name_remove == "exit":
                print("Closing...")
                time.sleep(2)
                sys.exit()

            if game_name_remove == "back":
                clear_console()
                continue

            updated_games = []
            found = False

            with open("games.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[0] == game_name_remove:
                        found = True
                    else:
                        updated_games.append(row)
            if found:
                with open("games.csv", "w") as file:
                    writer = csv.writer(file)
                    writer.writerows(updated_games)
                print(
                    f"{game_name_remove.title()} has been removed from your Game List.\n"
                )
                time.sleep(2)
                clear_console()
            else:
                print(f"{game_name_remove.title()} not found in your Game List.\n")
                time.sleep(2)
                clear_console()

        # Change game from incomplete to completed
        elif select[0] == "4" or "change game" in select:
            clear_console()
            print("\n=-- Change Game Completion --=\n\n")
            print(
                'Enter name of game. Type "exit" to quit or "back" to go to menu\n-----------------------------'
            )
            update_game = input("> ").strip().lower()

            if update_game == "exit":
                print("Closing...")
                time.sleep(2)
                sys.exit()

            if update_game == "back":
                clear_console()
                continue

            found = False
            updated_lines = []

            try:
                with open("games.csv", "r") as file:
                    games_reader = csv.reader(file)
                    for row in games_reader:
                        if row and row[0].strip().lower() == update_game:
                            current_status = row[1].strip().lower()
                            new_status = "False" if current_status == "true" else "True"
                            row[1] = new_status
                            found = True
                            print(
                                f"Updated {update_game.title()} status to {'Completed' if new_status == 'True' else 'Incomplete'}"
                            )
                            time.sleep(2)
                            clear_console()

                        updated_lines.append(row)

                if found:
                    with open("games.csv", "w") as file:
                        writer = csv.writer(file)
                        writer.writerows(updated_lines)
                else:
                    print(f"{update_game.title()} was not found in your games list")
                    time.sleep(2)
                    clear_console()

            except FileNotFoundError:
                print(
                    "The file 'games.csv' was not found. Please make sure it exists and you have added a game"
                )
                time.sleep(4)
                clear_console()

        # Show Reviews
        elif select[0] == "5" or "view review" in select:
            clear_console()
            print("\n=-- Show Reviews --=\n")

            games_with_reviews = []

            try:
                with open("reviews.csv", "r") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row:
                            game_name = row[0].strip().lower()
                            games_with_reviews.append(game_name)
            except FileNotFoundError:
                print("No reviews found. Please add reviews first.")
                time.sleep(2)
                clear_console()
                break

            if games_with_reviews:
                for game in games_with_reviews:
                    print(f"- {game.title()}")

            print(
                '\nEnter name of game. Type "exit" to quit or "back" to go to menu\n-----------------------------'
            )
            view_review = input("> ").strip().lower()

            if view_review == "exit":
                print("Closing...")
                time.sleep(1)
                sys.exit()

            elif view_review == "back":
                clear_console()
                continue

            found = False
            review_content = None

            try:
                with open("reviews.csv", "r") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row and row[0] == view_review:
                            found = True
                            review_content = row[1]
                            review_score = row[2]
                            break
            except FileNotFoundError:
                pass

            if found:
                clear_console()
                print(f"-----{view_review.title()} Review-----\n")
                print(f"Review: {review_content}")
                print(f"Score: {review_score}")
                while True:
                    back = input('\nType "back" to return to menu: ').strip().lower()
                    if back == "back":
                        clear_console()
                        break
                    else:
                        print("Unknown Command")
                        time.sleep(2)
                        clear_console()
                        continue
            else:
                print(
                    f"\nA review for {view_review.title()} was not found in your reviews."
                )
                print("\n\n--Returning to Menu--")
                time.sleep(5)
                clear_console()

        # Add Reviews
        elif select[0] == "6" or "add review" in select:
            clear_console()
            print("\n=-- Add Review --=\n\n")
            print(
                'Enter name of game. Type "exit" to quit or "back" to go to menu\n-----------------------------'
            )
            game_name_review = input("> ").strip().lower()

            if game_name_review == "exit":
                print("Closing...")
                time.sleep(1)
                sys.exit()

            elif game_name_review == "back":
                clear_console()
                continue

            found = False

            with open("games.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[0] == game_name_review:
                        found = True
                        break

            if found:
                print(f"What are your thoughts on {game_name_review.title()}?\n")
                review = input("> ")

                while True:
                    try:
                        score = float(
                            input(
                                f"\nRate {game_name_review.title()} out of 10: "
                            ).strip()
                        )
                        if 0 <= score <= 11:
                            break
                        else:
                            print("Invalid Rating. Try a number 0-10 (or 11)")
                    except ValueError:
                        print("Error. Check Input. Numbers Only")

                with open("reviews.csv", "a") as file:
                    writer = csv.writer(file)
                    writer.writerow([game_name_review, review, score])

                print(
                    f"Your review and score for {game_name_review.title()} have been saved.\n"
                )
                time.sleep(2)
                clear_console()
            else:
                print(f"{game_name_review.title()} not found in your Game List. \n")
                time.sleep(2)
                clear_console()

        # Exit Program
        elif select[0] == "7" or "exit" in select:
            clear_console()
            print("Bye!", end="", flush=True)
            time.sleep(1)
            sys.exit()

        # Error
        else:
            print("Error. Input a number or type your selection.")
            time.sleep(2)
            clear_console()
            continue


def random_color():
    return random.choice(colors)



if __name__ == "__main__":
    main()
