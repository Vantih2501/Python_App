import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
FPS = 60
PRESENT_WIDTH = 50
PRESENT_HEIGHT = 80
CAR_WIDTH = 50
CAR_HEIGHT = 80
SCORE_FONT_SIZE = 30
ROAD_LEFT_BOUND = 100
ROAD_RIGHT_BOUND = SCREEN_WIDTH - 100
SCROLL_SPEED = 5
CAR_SPAWN_RATE = 50

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Don't Touch My Present")

# Load images
def load_and_scale_image(path, size):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, size)

main_car = load_and_scale_image("assets/main_car.png", (PRESENT_WIDTH, PRESENT_HEIGHT))
truck_images = [
    load_and_scale_image("assets/blue_truck_car.png", (CAR_WIDTH, CAR_HEIGHT)),
    load_and_scale_image("assets/white_truck_car.png", (CAR_WIDTH, CAR_HEIGHT)),
    load_and_scale_image("assets/green_truck_car.png", (CAR_WIDTH, CAR_HEIGHT)),
]
asphalt_image = load_and_scale_image("assets/road.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
left_building_image = load_and_scale_image("assets/left_building.png", (100, SCREEN_HEIGHT))
right_building_image = load_and_scale_image("assets/right_building.png", (100, SCREEN_HEIGHT))

# Classes
class Present:
    def __init__(self):
        self.rect = main_car.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        self.speed = 5

    def move(self, dx):
        self.rect.x += dx
        self.rect.x = max(ROAD_LEFT_BOUND, min(self.rect.x, ROAD_RIGHT_BOUND - PRESENT_WIDTH))

class Car:
    def __init__(self):
        self.image = random.choice(truck_images)
        x_position = random.randint(ROAD_LEFT_BOUND, ROAD_RIGHT_BOUND - CAR_WIDTH)
        self.rect = self.image.get_rect(center=(x_position, 0))

    def move(self):
        self.rect.y += SCROLL_SPEED
        return self.rect.y > SCREEN_HEIGHT

# Helper functions
def is_overlapping(new_car_rect):
    return any(new_car_rect.colliderect(car.rect) for car in cars)

def draw_background(asphalt_y):
    screen.blit(asphalt_image, (0, asphalt_y))
    screen.blit(asphalt_image, (0, asphalt_y - SCREEN_HEIGHT))
    screen.blit(left_building_image, (0, 0))
    screen.blit(right_building_image, (SCREEN_WIDTH - 100, 0))

def draw_score():
    font = pygame.font.Font(None, SCORE_FONT_SIZE)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

# Game variables
clock = pygame.time.Clock()
running = True
score = 0
cars = []
asphalt_y = 0
present = Present()

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        present.move(-present.speed)
    if keys[pygame.K_RIGHT]:
        present.move(present.speed)

    # Spawn cars
    if random.randint(1, CAR_SPAWN_RATE) == 1:
        new_car = Car()
        if not is_overlapping(new_car.rect):
            cars.append(new_car)

    # Move cars and check for collisions
    for car in cars[:]:
        if car.move():
            cars.remove(car)
            score += 1
        if present.rect.colliderect(car.rect):
            print(f"Game Over! Your score: {score}")
            running = False

    # Scroll the asphalt
    asphalt_y = (asphalt_y + SCROLL_SPEED) % SCREEN_HEIGHT

    # Drawing
    draw_background(asphalt_y)
    screen.blit(main_car, present.rect)
    for car in cars:
        screen.blit(car.image, car.rect)
    draw_score()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
