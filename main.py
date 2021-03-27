import turtle


def create_queries_component():
    queries_caption = """
    Choose an option from 1-7:
    1. Order of ladder on a specific date
    2. Data of challenges (based on player names)
    3. Data of challenges (based on data)
    4. List of matches a player has played
    5. Most active player
    6. Least active player
    7. List of matches played in a specific date range
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
