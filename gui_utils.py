import turtle


def click(x, y):
    button.hideturtle()
    button.write("Thank you!", align="center", font=("Arial", 18, "bold"))


screen = turtle.Screen()


button = turtle.Turtle()
turtle.hideturtle()
button.speed("fastest")
button.shape("square")
button.shapesize(2, 2)

button.penup()
button.goto(200, 200)
button.pendown()

button.fillcolor("gray")
button.onclick(click)
turtle.showturtle()

screen.mainloop()
