import turtle
import os

# Optionally import winsound if this is windows
if os.uname().sysname == "Windows":
    import winsound

# Setup window
wn = turtle.Screen()
wn.title = "Pong by Anthony Atkinson"
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

# Global variables used for game logic
y_max = (wn.window_height() / 2)
y_min = -1 * (wn.window_height() / 2)
x_max = (wn.window_width() / 2)
x_min = -1 * (wn.window_width() / 2)
game_y_max = y_max - 50

# Score
scores = {
    "a": 0,
    "b": 0
}

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape(name="square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(x=x_min + 50, y=0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape(name="square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(x=x_max - 50, y=0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape(name="square")
ball.color("white")
ball.penup()
ball.goto(x=0, y=0)
ball.dx = 2
ball.dy = 2

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(x=0, y=y_max - 40)


# Functions
def paddle_a_up():
    y = paddle_a.ycor()
    if y + 75 > game_y_max:
        return
    y += 20
    paddle_a.sety(y)


def paddle_a_down():
    y = paddle_a.ycor()
    if y - 75 < y_min:
        return
    y -= 20
    paddle_a.sety(y)


def paddle_b_up():
    y = paddle_b.ycor()
    if y + 75 > game_y_max:
        return
    y += 20
    paddle_b.sety(y)


def paddle_b_down():
    y = paddle_b.ycor()
    if y - 75 < y_min:
        return
    y -= 20
    paddle_b.sety(y)


def update_score(player=""):
    if player != "":
        scores[player] += 1
    pen.clear()
    score_text = "Player A: {}  Player B: {}".format(scores["a"], scores["b"])
    pen.write(score_text, align="center", font=("Courier", 24, "normal"))


def play_sound():
    os_name = os.uname().sysname
    if os_name == "Darwin":
        os.system("afplay bounce.wav &")
    elif os_name == "Linux":
        os.system("aplay bounce.wav &")
    elif os_name == "Windows":
        winsound.PlaySound("bound.wav", winsound.SND_ASYNC)


# Create keyboard bindings
wn.listen()
wn.onkeypress(fun=paddle_a_up, key="w")
wn.onkeypress(fun=paddle_a_down, key="s")
wn.onkeypress(fun=paddle_b_up, key="Up")
wn.onkeypress(fun=paddle_b_down, key="Down")

# Draw score on screen
update_score()

# Main game loop
while True:
    wn.update()
    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    paddle_a_x = paddle_a.xcor() + 13
    paddle_a_y_max = paddle_a.ycor() + 50
    paddle_a_y_min = paddle_a.ycor() - 50
    paddle_b_x = paddle_b.xcor() - 13
    paddle_b_y_max = paddle_b.ycor() + 50
    paddle_b_y_min = paddle_b.ycor() - 50

    # Wall Border Checking
    if ball.ycor() > game_y_max or ball.ycor() < (y_min + 13):
        ball.dy *= -1
        play_sound()
    # Hit the edge of the screen
    elif ball.xcor() > (x_max - 13) or ball.xcor() < (x_min + 13):
        ball.goto(x=0, y=0)
        if ball.dx > 0:
            update_score("a")
        else:
            update_score("b")
        ball.dx *= -1

    # Ball hits paddle
    if (ball.xcor() < paddle_a_x and paddle_a_y_max >= ball.ycor() >= paddle_a_y_min) or \
            (ball.xcor() > paddle_b_x and paddle_b_y_max >= ball.ycor() >= paddle_b_y_min):
        ball.dx *= -1
        play_sound()
