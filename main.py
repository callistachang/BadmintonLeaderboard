import turtle
import actions
from gui_utils import *


### CONSTANTS ###

WIDTH = 900
HEIGHT = 1000
COL_1_X = 10
COL_2_X = 280
COL_3_X = 570
ROW_1_Y = HEIGHT - 75
ROW_2_Y = HEIGHT - 340
COL_3_OFFSET_Y = 10
MENU_SPACING_Y = 80
HEADING_SPACING_Y = 40
LADDER_SPACING_Y = 32
COL_3_SPACING_Y = 44


### COMPONENTS ###


def error_alert(text):
    turtle.textinput("Error", text)


def display_component():
    ### MENU ###

    create_text_heading((COL_1_X, ROW_1_Y + HEADING_SPACING_Y), "Menu")
    create_button(
        (COL_1_X, ROW_1_Y),
        "Make Query",
        actions.get_leaderboard,
    )
    create_button(
        (COL_1_X, ROW_1_Y - MENU_SPACING_Y),
        "Create Challenge",
        actions.get_leaderboard,
    )
    create_button(
        (COL_1_X, ROW_1_Y - MENU_SPACING_Y * 2),
        "Add Challenge Results",
        actions.get_leaderboard,
    )
    create_button(
        (COL_1_X, ROW_1_Y - MENU_SPACING_Y * 3),
        "Register Player",
        new_player_component,
    )
    create_button(
        (COL_1_X, ROW_1_Y - MENU_SPACING_Y * 4),
        "Withdraw Player",
        actions.get_leaderboard,
    )

    ### LEADERBOARD ###

    ladder = actions.get_leaderboard()

    create_text_heading((COL_2_X, ROW_1_Y + HEADING_SPACING_Y), "Ladder (Top 25)")
    for i in range(len(ladder)):
        create_rectangle_one_line((COL_2_X, ROW_1_Y - LADDER_SPACING_Y * i), ladder[i])

    ### MOST RECENT CHALLENGES (most recent 5) ###

    most_recent_challenges = actions.get_most_recent_challenges()
    # print(most_recent_challenges)

    create_text_heading(
        (COL_3_X, ROW_1_Y + HEADING_SPACING_Y), "Most Recent (Latest 5)"
    )
    for i in range(len(most_recent_challenges)):
        challenger, opponent, date, score = most_recent_challenges[i]
        create_rectangle_two_lines(
            (COL_3_X, (ROW_1_Y - COL_3_OFFSET_Y) - COL_3_SPACING_Y * i),
            f"{challenger} v {opponent}",
            f"{date} | {score}",
        )

    ### YET TO PLAY CHALLENGES ###

    yet_to_play_challenges = actions.get_yet_to_play_challenges()
    # print(yet_to_play_challenges)

    create_text_heading((COL_3_X, ROW_2_Y + HEADING_SPACING_Y), "Yet To Play")
    for i in range(len(yet_to_play_challenges)):
        challenger, opponent, date = yet_to_play_challenges[i]
        rectangle_y = (ROW_2_Y - COL_3_OFFSET_Y) - COL_3_SPACING_Y * i
        create_rectangle_two_lines(
            (COL_3_X, rectangle_y), f"{challenger} v {opponent}", date
        )


def new_player_component():
    name = turtle.simpledialog.askstring("Add New Player", "Name of new player:")
    if name is None:
        error_alert("Player exists in database")
    else:
        actions.register_new_player(name)
        refresh_screen()


def remove_player_component():
    name = turtle.simpledialog.askstring(
        "Remove Player", "Name of player to be removed:"
    )
    if name is None:
        error_alert("Player doesn't exist in database")
    else:
        actions.withdraw_player(name)
        refresh_screen()


def new_challenge_component():
    from datetime import datetime

    player_list = actions.get_leaderboard()
    challenger = turtle.simpledialog.askstring(
        "New Challenge - Challenger", "Name of challenger:"
    )
    opponent = turtle.simpledialog.askstring(
        "New Challenge - Opponent",
        "Name of opponent (at most 3 rankings higher than the challenger):",
    )
    date = turtle.simpledialog.askstring(
        "New Challenge - Date",
        "Date of challenge (DD-MM-YYYY, must be today or later):",
    )
    date_obj = actions._convert_string_to_datetime_obj(date)
    if challenger not in player_list:
        error_alert(f"'{challenger}' doesn't exist in database")
    if opponent not in player_list:
        error_alert(f"'{opponent}' doesn't exist in database")
    if not date_obj:
        error_alert("Invalid date format")
    elif date_obj < datetime.today():
        error_alert("Date entered should be today or later")
    else:
        actions.create_challenge(challenger, opponent, date)
        refresh_screen()


def challenge_results_component():
    player_list = actions.get_leaderboard()
    challenger = turtle.simpledialog.askstring(
        "Record Challenge - Challenger", "Name of challenger:"
    )
    opponent = turtle.simpledialog.askstring(
        "Record Challenge - Opponent", "Name of opponent:"
    )
    date = turtle.simpledialog.askstring(
        "Record Challenge - Date", "Date of challenge (DD-MM-YYYY):"
    )
    results = turtle.simpledialog.askstring(
        "Record Challenge - Date", "Scores ('xx-xx xx-xx' OR 'xx-xx xx-xx xx-xx')"
    )
    success = actions.record_challenge_result(challenger, opponent, date, results)
    if success:
        refresh_screen()
    else:
        error_alert("No challenge could be found")


def queries_component():
    queries_caption = """
    Choose an option from 1-7:
    1. Order of ladder on a specific date
    2. Data of challenges (based on player names)
    3. Data of challenges (based on data)
    4. List of matches a player has played
    5. Most active player
    6. Least active player
    7. List of matches played in a specific date range
    8. Player with the most wins
    """
    is_error_message_shown = False
    is_done_querying = False

    while not is_done_querying:
        option = turtle.simpledialog.askinteger("Make Query", queries_caption)
        # ensure that the value put in is within the options
        if option is None:
            break
        elif option and 1 <= option <= 7:
            # break out of the loop if querying is successful
            is_done_querying = True
        else:
            # if not, append an error message to be shown
            if not is_error_message_shown:
                queries_caption += "\nPlease enter a valid option"
                is_error_message_shown = True

    if option == 1:
        pass
    elif option == 2:
        pass
    elif option == 3:
        pass
    elif option == 4:
        pass
    elif option == 5:
        pass
    elif option == 6:
        pass
    elif option == 7:
        pass


def check_if_menu_buttons_clicked(x, y):
    if COL_1_X <= x <= (COL_1_X + 20):
        if (ROW_1_Y) <= y <= (ROW_1_Y + 20):
            pass
        elif (ROW_1_Y - MENU_SPACING_Y) <= y <= (ROW_1_Y - MENU_SPACING_Y + 20):
            new_challenge_component()
        elif (ROW_1_Y - MENU_SPACING_Y * 2) <= y <= (ROW_1_Y - MENU_SPACING_Y * 2 + 20):
            challenge_results_component()
        elif (ROW_1_Y - MENU_SPACING_Y * 3) <= y <= (ROW_1_Y - MENU_SPACING_Y * 3 + 20):
            new_player_component()
        elif (ROW_1_Y - MENU_SPACING_Y * 4) <= y <= (ROW_1_Y - MENU_SPACING_Y * 4 + 20):
            remove_player_component()


def refresh_screen():
    screen.clear()
    screen.tracer(False)
    display_component()
    screen.onscreenclick(check_if_menu_buttons_clicked)


### SCREEN SETUP ###

if __name__ == "__main__":
    screen = turtle.Screen()
    screen.tracer(False)
    screen.setup(WIDTH, HEIGHT)
    screen.mode("world")
    screen.setworldcoordinates(0, 0, WIDTH, HEIGHT)
    display_component()
    screen.onscreenclick(check_if_menu_buttons_clicked)
    screen.update()
    screen.mainloop()
