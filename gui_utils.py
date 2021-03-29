import turtle
import actions

# from main import draw_components


def create_button(coords, text, on_click_function, *args):
    FONT = ("Arial", 10, "bold")
    rectangle = turtle.Turtle(visible=False)
    rectangle.speed("fastest")
    rectangle.penup()
    rectangle.goto(coords[0], coords[1])

    # draw box
    rectangle.fillcolor("blue")
    rectangle.begin_fill()
    for _ in range(2):
        rectangle.forward(20)
        rectangle.left(90)
        rectangle.forward(20)
        rectangle.left(90)
    rectangle.end_fill()

    # write text on box
    rectangle.write("     " + text, align="left", font=FONT)


def create_text_heading(coords, text):
    FONT = ("Arial", 14, "bold")
    heading = turtle.Turtle(visible=False)
    heading.speed("fastest")
    heading.penup()
    heading.goto(coords[0], coords[1])
    heading.write(text, font=FONT)


def create_rectangle_one_line(coords, text):
    FONT = ("Arial", 10, "normal")
    rectangle = turtle.Turtle(visible=False)
    rectangle.speed("fastest")
    rectangle.penup()
    rectangle.goto(coords[0], coords[1])

    # draw box
    rectangle.fillcolor("lightgrey")
    rectangle.begin_fill()
    for _ in range(2):
        rectangle.forward(220)
        rectangle.left(90)
        rectangle.forward(28)
        rectangle.left(90)
    rectangle.end_fill()

    # write text on box
    rectangle.write(" " + text, align="left", font=FONT)


def create_rectangle_two_lines(coords, text1, text2):
    BIG_FONT = ("Arial", 10, "bold")
    SMALL_FONT = ("Arial", 10, "normal")
    rectangle = turtle.Turtle(visible=False)
    rectangle.speed("fastest")
    rectangle.penup()
    rectangle.goto(coords[0], coords[1])

    # draw box
    rectangle.fillcolor("lightgrey")
    rectangle.begin_fill()
    for _ in range(2):
        rectangle.forward(248)
        rectangle.left(90)
        rectangle.forward(40)
        rectangle.left(90)
    rectangle.end_fill()

    # write text on box
    rectangle.sety(coords[1] + 18)
    rectangle.write(" " + text1, align="left", font=BIG_FONT)
    rectangle.sety(coords[1])
    rectangle.write(" " + text2, align="left", font=SMALL_FONT)
    pass
