import turtle
import actions
from gui_utils import create_button, create_text_heading, create_rectangle_one_line

screen = turtle.Screen()

### CONSTANTS ###
START_X = -450 
START_Y = 320 
MENU_Y_SPACING = 80
HEADING_Y_SPACING = 40 
LADDER_Y_SPACING = 40
LADDER_START_X = -200 

### MENU ###
create_text_heading((START_X, START_Y + HEADING_Y_SPACING), "Menu")
create_button(
    (START_X, START_Y),
    "Make Query",
    actions.get_leaderboard,
)
create_button(
    (START_X, START_Y - MENU_Y_SPACING),
    "Create Challenge",
    actions.get_leaderboard,
)
create_button(
    (START_X, START_Y - MENU_Y_SPACING * 2),
    "Add Challenge Results",
    actions.get_leaderboard,
)
create_button(
    (START_X, START_Y - MENU_Y_SPACING * 3),
    "Register Player",
    actions.get_leaderboard,
)
create_button(
    (START_X, START_Y - MENU_Y_SPACING * 4),
    "Withdraw Player",
    actions.get_leaderboard,
)

### LEADERBOARD ###
create_text_heading((LADDER_START_X, START_Y + HEADING_Y_SPACING), "Ladder")
ladder = actions.get_leaderboard()
for i, record in enumerate(ladder):
    create_rectangle_one_line((LADDER_START_X, START_Y - LADDER_Y_SPACING*i), "asdfk")

### MOST RECENT CHALLENGES (most recent 5) ###
create_text_heading((100, START_Y + LADDER_Y_SPACING), "Most Recent Challenges")


### YET TO PLAY CHALLENGES ###

# create_text_heading((100, 200), "waddup")
screen.mainloop()
