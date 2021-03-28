import turtle

def create_button(coords, text, on_click_function, *args):
    def draw_onclick(x, y):
        on_click_function(*args)

    FONT = ("Arial", 12, "bold")
    button = turtle.Turtle(visible=False)
    button.speed("fastest")
    button.penup()
    button.goto(coords[0], coords[1])

    # draw box
    button.fillcolor("cyan")
    button.begin_fill()
    for _ in range(2):
        button.forward(220)
        button.left(90)
        button.forward(28)
        button.left(90)
    button.end_fill()

    # register function
    button.onclick(draw_onclick)
    # write text on box 
    button.write(text, align="left", font=FONT)

def create_text_heading(coords, text):
    FONT = ("Arial", 14, "bold")
    heading = turtle.Turtle(visible=False)
    heading.speed("fastest")
    heading.penup()
    heading.goto(coords[0], coords[1])
    heading.write(text, font=FONT)


def create_rectangle_one_line(coords, text):
    FONT = ("Arial", 10, "normal")
    button = turtle.Turtle(visible=False)
    button.speed("fastest")
    button.penup()
    button.goto(coords[0], coords[1])

    # draw box
    button.fillcolor("lightgrey")
    button.begin_fill()
    for _ in range(2):
        button.forward(220)
        button.left(90)
        button.forward(28)
        button.left(90)
    button.end_fill()

    # write text on box 
    button.write(text, align="left", font=FONT)

def create_rectangle_two_lines(coords, text1, text2):
    pass


def create_query_dialog():
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


# def create_leaderboard_rectangle(coords, height, text1):
#     pass

# def click(x, y):
#     button.hideturtle()
#     button.write("Thank you!", align="center", font=("Arial", 18, "bold"))


# screen = turtle.Screen()


# button = turtle.Turtle()
# turtle.hideturtle()
# button.speed("fastest")
# button.shape("square")
# button.shapesize(2, 2)

# button.penup()
# button.goto(200, 200)
# button.pendown()

# button.fillcolor("gray")
# button.onclick(click)
# turtle.showturtle()

# screen.mainloop()
