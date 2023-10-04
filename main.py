# Top 10 things I will never use again
# 1. Pygame
# 2. Pygame
# 3. Pygame
# 4. Pygame
# 5. Pygame
# 6. Pygame
# 7. Pygame
# 8. Pygame
# 9. Pygame
# 10. Pygame
import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from math import cos, sin, radians, pi


# Gravitational constant
G = 9.82
# Air density
AD = 1.3
# Drag coefficient
DG = 0.47
# Pixels to Metres
SCALE = 5
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))


def vec2(length, angle) -> pygame.Vector2:
    angle_rad = radians(-angle)
    x = length * cos(angle_rad)
    y = length * sin(angle_rad)
    return pygame.Vector2(x, y)


class ThrowableObject:
    pos: pygame.Vector2
    velocity: pygame.Vector2
    volume: float
    radius: float
    mass: float
    trail: pygame.Surface

    def __init__(self, pos: pygame.Vector2, velocity, angle, radius, mass):
        self.pos = pos
        self.velocity = vec2(velocity, angle)
        self.volume = (4 * pi * radius**3) / 3
        self.radius = radius
        self.mass = mass
        self.trail = pygame.Surface((WIDTH, HEIGHT))
        self.move_since_last_point = 0

    def update_velocity(self, dt, wind_velocity):
        buoyancy_acceleration = (AD * self.volume * G) / self.mass
        delta_wind: pygame.Vector2 = self.velocity - wind_velocity

        area = self.radius**2 * pi
        wind_acceleration_x = 0.5 * AD * (delta_wind.x**2) * DG * area / self.mass
        wind_acceleration_y = 0.5 * AD * (delta_wind.y**2) * DG * area / self.mass

        try:
            x_sig = (delta_wind.x) / (abs(delta_wind.x))
        except:
            x_sig = 1
        try:
            y_sig = (delta_wind.y) / (abs(delta_wind.y))
        except:
            y_sig = 1
        y_acceleration = G - buoyancy_acceleration - y_sig * wind_acceleration_y
        x_acceleration = -wind_acceleration_x * x_sig

        self.velocity.x += x_acceleration * dt
        self.velocity.y += y_acceleration * dt

    def update_position(self, dt):
        self.pos += self.velocity * dt * SCALE
        self.move_since_last_point += (self.velocity * dt).length()

    def check_collision(self):
        if self.pos.y >= screen.get_height() - self.radius - 20:
            self.velocity.y *= -0.9
            self.pos.y = screen.get_height() - self.radius - 20
            print(self.pos.x / SCALE)

    def update(self, dt, wind_velocity):
        if self.move_since_last_point * SCALE > 10.0:
            self.move_since_last_point = 0.0
            pygame.draw.circle(self.trail, "red", self.pos, 2)

        self.update_velocity(dt, wind_velocity)
        self.update_position(dt)
        self.check_collision()

    def draw(self, dt, wind_velocity):
        draw_size = max(min(self.radius * SCALE * 10, 10), 3)
        pygame.draw.circle(screen, "black", self.pos, draw_size)
        screen.blit(self.trail, (0, 0))
        if dt != 0:
            self.update(dt, wind_velocity)
        pygame.draw.circle(screen, "white", self.pos, draw_size)


class UI:
    wind_angle: Slider
    wind_length: TextBox
    velocity_angle: Slider
    velocity_length: TextBox
    height: Slider
    value_spots: list[int]

    def __init__(self):
        self.value_spots = []
        width = 100
        padding = 10
        x = WIDTH - width + padding
        font_size = 24
        title_size = 32
        title_font = pygame.font.SysFont("", title_size)
        font = pygame.font.SysFont("", font_size)
        text_surface = pygame.Surface((100, HEIGHT))
        text_surface.fill("#808080")
        y = 50

        text_surface.fill("black", pygame.Rect(0, y, width, 2))
        y += 4

        title_txt = title_font.render("Start", False, "black")
        text_surface.blit(title_txt, (padding / 2, y))
        y += title_size

        txt = font.render("Angle: ", False, "black")
        text_surface.blit(txt, (padding, y))
        y += font_size

        self.velocity_angle = Slider(
            screen,
            x,
            y,
            width - padding * 2,
            10,
            min=0,
            max=360,
            handleColour=(255, 255, 255),
            initial=0,
        )
        y += 15

        self.value_spots.append(y)
        y += font_size

        txt = font.render("Velocity: ", False, "black")
        text_surface.blit(txt, (padding, y))
        y += font_size

        self.velocity_length = TextBox(screen, x, y, width - padding * 2, font_size + 2)
        self.velocity_length.setText("30")
        y += font_size + 2 + 5

        txt = font.render("Mass (kg): ", False, "black")
        text_surface.blit(txt, (padding, y))
        y += font_size

        self.mass = TextBox(screen, x, y, width - padding * 2, font_size + 2)
        self.mass.setText("70")
        y += font_size + 2 + 5

        txt = font.render("Radius (m): ", False, "black")
        text_surface.blit(txt, (padding, y))
        y += font_size

        self.radius = TextBox(screen, x, y, width - padding * 2, font_size + 2)
        self.radius.setText("0.3")
        y += font_size + 2 + 5

        title_txt = title_font.render("Height", False, "black")
        text_surface.blit(title_txt, (padding / 2, y))
        y += title_size

        self.height = Slider(
            screen,
            x,
            y,
            width - padding * 2,
            10,
            min=0,
            max=HEIGHT - 20,
            handleColour=(255, 255, 255),
        )
        y += 15

        self.value_spots.append(y)
        y += font_size

        text_surface.fill("black", pygame.Rect(0, y, width, 2))
        y += 4

        title_txt = title_font.render("Wind", False, "black")
        text_surface.blit(title_txt, (padding / 2, y))
        y += title_size

        txt = font.render("Angle: ", False, "black")
        text_surface.blit(txt, (padding, y))
        y += font_size

        self.wind_angle = Slider(
            screen,
            x,
            y,
            width - padding * 2,
            10,
            min=0,
            max=360,
            handleColour=(255, 255, 255),
        )
        y += 15

        self.value_spots.append(y)
        y += font_size

        txt = font.render("Velocity: ", False, "black")
        text_surface.blit(txt, (padding, y))
        y += font_size

        self.wind_length = TextBox(screen, x, y, width - padding * 2, font_size + 2)
        self.wind_length.setText("0")
        y += font_size + 2 + 5

        text_surface.fill("black", pygame.Rect(0, y, width, 2))
        y += 4

        self.text = text_surface

    def update(self, events):
        font = pygame.font.SysFont("", 20)
        screen.blit(self.text, (WIDTH - 100, 0))

        angle = self.velocity_angle.getValue()
        txt = font.render(f"{angle}", False, "black")
        screen.blit(txt, (WIDTH - 100 + 10, self.value_spots[0]))

        height = self.height.getValue()
        height /= SCALE
        txt = font.render(f"{height}m", False, "black")
        screen.blit(txt, (WIDTH - 100 + 10, self.value_spots[1]))

        angle = self.wind_angle.getValue()
        txt = font.render(f"{angle}", False, "black")
        screen.blit(txt, (WIDTH - 100 + 10, self.value_spots[2]))

        pygame_widgets.update(events)


class Environment:
    obj: ThrowableObject
    wind: pygame.Vector2
    ui: UI

    def __init__(self):
        self.obj = ThrowableObject(pygame.Vector2(10, 0), 0, 0, 0, 0)
        self.wind = pygame.Vector2(0, 0)
        self.ui = UI()

    def draw(self, dt):
        self.obj.draw(dt, self.wind)

    def update_wind(self):
        try:
            wind_angle: int = self.ui.wind_angle.getValue()
            wind_length = float(self.ui.wind_length.getText())
            self.wind = vec2(wind_length, wind_angle)
        except:
            pass

    def update_mass(self):
        try:
            mass = float(self.ui.mass.getText())
            if mass == 0.0:
                raise ValueError
            self.obj.mass = mass
        except:
            pass

    def update_radius(self):
        try:
            radius = float(self.ui.radius.getText())
            if radius == 0.0:
                raise ValueError
            self.obj.radius = radius
        except:
            pass

    def update_velocity(self):
        try:
            vel_angle: int = self.ui.velocity_angle.getValue()
            vel_length = float(self.ui.velocity_length.getText())
            self.obj.velocity = vec2(vel_length, vel_angle)
        except:
            pass

    def update_height(self):
        try:
            height = self.ui.height.getValue()
            self.obj.pos.y = HEIGHT - height - 20
        except:
            pass

    def setup(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            events = pygame.event.get()
            for event in events:
                # Exit
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    # Start
                    if event.key == pygame.K_RETURN:
                        running = self.run()
                        del self.obj
                        self.obj = ThrowableObject(pygame.Vector2(10, 0), 0, 0, 0, 0)
            clock.tick(200)
            self.update_wind()
            self.update_mass()
            self.update_radius()
            self.update_velocity()
            self.update_height()
            self.draw(0)
            pygame.draw.rect(screen, "darkgreen", pygame.Rect(0, 700, 1280, 20))
            self.ui.update(events)
            pygame.display.flip()

    def reset(self):
        del self.obj
        self.obj

    def run(self) -> bool:
        clock = pygame.time.Clock()
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                # Exit
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    # Reset
                    if event.key == pygame.K_r:
                        running = False
            dt = clock.tick(100) / 1000
            self.draw(dt)
            pygame.draw.rect(screen, "darkgreen", pygame.Rect(0, 700, 1280, 20))
            self.ui.update(events)
            pygame.display.flip()
        return True


# pygame setup
pygame.init()

env = Environment()

env.setup()

pygame.quit()
