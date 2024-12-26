import turtle
import random
import time
import math

class Dot(turtle.Turtle):
    DOT_COLOURS = (
        "#fdb33b", "#6d227a", "#fff3e6",
        "#a3c9f1", "#d1e2dc", "#f5b5d6",
        "#c8e0d6", "#f0c9c0", "#f7d8c1",
        "#b7e4c7", "#f4e1d2", "#f9c2c4",
        "#fce0cb", "#d0b2d8", "#d9f8d7",
        "#f2a7d9", "#ff99cc", "#ff66b2", "#ff3399"
    )

    def __init__(self, x, y, size_range):
        super().__init__()
        self.shape("circle")
        self.base_color = random.choice(self.DOT_COLOURS)
        self.color(self.base_color)
        self.penup()
        self.setposition(x, y)
        self.current_size = random.uniform(size_range[0], size_range[1])
        self.shapesize(self.current_size)
        self.shrink_rate = random.uniform(0.004, 0.009)
        self.min_size = 0.1
        self.transparency = 1.0
        self.creation_time = time.time()
        self.target_x = 0
        self.target_y = 0
        self.recycled = False

    def shrink_and_fall(self, dissolve_time):
        elapsed_time = time.time() - self.creation_time
        if elapsed_time > dissolve_time:
            if self.current_size > self.min_size:
                self.current_size -= self.shrink_rate
                self.shapesize(self.current_size)
                self.transparency -= 0.1 / 5
                self.move_towards_center()
                if self.transparency <= 0:
                    self.hideturtle()
                    self.recycled = True
                    return True
                faded_color = self.fade_color(self.base_color, self.transparency)
                self.color(faded_color)
        else:
            return False
        return False

    def fade_color(self, color, transparency):
        rgb = tuple(int(color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        faded_rgb = tuple(int(c * transparency + 255 * (1 - transparency)) for c in rgb)
        return f"#{''.join(f'{v:02x}' for v in faded_rgb)}"

    def move_towards_center(self):
        step_size = 2
        x_diff = self.target_x - self.xcor()
        y_diff = self.target_y - self.ycor()
        distance = math.sqrt(x_diff**2 + y_diff**2)

        if distance > step_size:
            move_x = (x_diff / distance) * step_size
            move_y = (y_diff / distance) * step_size
            self.setx(self.xcor() + move_x)
            self.sety(self.ycor() + move_y)
        else:
            self.setposition(self.target_x, self.target_y)

    def reset_position(self, new_x, new_y):
        self.setposition(new_x, new_y)
        self.transparency = 1.0
        self.current_size = random.uniform(0.2, 0.5)
        self.shapesize(self.current_size)

BACKGROUND_COLOURS = "#1a6b72"
dot_size_range = 0.2, 0.5
frame_rate = 120

window = turtle.Screen()
window.tracer(0)
window.bgcolor(BACKGROUND_COLOURS)

lead_dot = turtle.Turtle()
lead_dot.shape("circle")
lead_dot.color("white")
lead_dot.penup()

dots = []
interval_start = 0
delay = 0.05

angle = 0
radius_multiplier = 100
center_x, center_y = 0, 200
circle_count = 0

def polar_heart(t):
    sin_t = math.sin(t)
    cos_t = math.cos(t)
    r = (
        (sin_t * math.sqrt(abs(cos_t))) / (sin_t + 7 / 5)
        - 2 * sin_t
        + 2
    )
    return r

def heart_position(t):
    r = polar_heart(t)
    x = r * math.cos(t)
    y = r * math.sin(t)
    return x * radius_multiplier, y * radius_multiplier

while True:
    start_frame_time = time.time()

    angle_rad = math.radians(angle)
    x, y = heart_position(angle_rad)
    lead_dot.setposition(center_x + x, center_y + y)

    angle += 0.534
    if angle >= 360:
        angle = 0
        circle_count += 1

    if circle_count >= 2:
        delay = 0.005
        dissolve_time = 10
    else:
        dissolve_time = 10

    if time.time() - interval_start > delay:
        interval_start = time.time()
        dots.append(Dot(lead_dot.xcor(), lead_dot.ycor(), dot_size_range))

    for dot in dots[:]:
        if dot.shrink_and_fall(dissolve_time):
            if dot.recycled:
                angle_rad = math.radians(angle)
                new_x, new_y = heart_position(angle_rad)
                dot.reset_position(center_x + new_x, center_y + new_y)
                dot.recycled = False
            else:
                dots.remove(dot)

    window.update()

    frame_time = time.time() - start_frame_time
    if frame_time < 1 / frame_rate:
        time.sleep(1 / frame_rate - frame_time)
