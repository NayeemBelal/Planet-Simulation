from turtle import width
import pygame
import math
pygame.init()

# init my window
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

FONT = pygame.font.SysFont("comicsans", 16)
# rgb values for color
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80,78,81)
WHITE = (255,255,255)

class Planet:
    # all the constants I need 
    AU = 149.6e6*1000 # distance to sun from earth in meters
    G = 6.67428e-11 # G value to mesure the attractiom between objects 
    SCALE = 190 / AU # down to scale from meters to pixels 1AU = 100 pixels
    TIMESTEP = 3600*24 # how much time is elapsed in a frame 1DAY

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass


        self.orbit = []
        self.isSun = False
        self.distanceToSun = 0 # distance to sun
        self.x_vel = 0
        self.y_vel = 0 # speeds of planet
    
    # Draw a planet in the center of win when given colo and radius
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2 # the x and why are differnt for each planet
        y = self.y * self.SCALE + HEIGHT / 2 # sclaed brings it to the center

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x,y = point
                x = x * self.SCALE + WIDTH / 2 # point at x and y
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x,y)) #append it to list and use it as points on a line
        
            pygame.draw.lines(win, self.color, False, updated_points, 2) # draw a line
        pygame.draw.circle(win, self.color, (x,y), self.radius) # draw my planet as a circle

        # draw the distance from the sun on each planet
        if not self.isSun:
            distance_text = FONT.render(f"{round(self.distanceToSun/1000)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2,y - distance_text.get_height()/2))
    # math for movement of planets
    def attraction(self, other):
        # other is the name of the planet we are caluclating attraction with
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x 
        distance_y = other_y - self.y # findng the x and y distances
        distance = math.sqrt(distance_x**2 + distance_y**2) # finding the actual distance
        if other.isSun:
            self.distanceToSun = distance # if other planet is the sun, then the distnace is just 0
        force = self.G * self.mass * other.mass / distance**2 # calculate the force of attraction
        angle = math.atan2(distance_y, distance_x) # angle between the two forces
        force_x = math.cos(angle) * force
        force_y = math.sin(angle) * force #horizontal and vertical forces
        return force_x, force_y

    # change xvel and yvel
    def update_position(self, planets):
        total_fx = total_fy = 0 # total forces of all planets
        for planet in planets:
            if self == planet:
                continue # if my planet is being compqred to itself, it would give an error cuz there is not distance
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy # adding the change in forces
        self.x_vel += total_fx / self.mass * self.TIMESTEP # accel = f/m
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x,self.y))

# main function
def main():
    run = True

    clock = pygame.time.Clock() # to keep my framerate constant
    # init all the things I am drawing on the window - planets and sun
    sun = Planet(0,0,30, YELLOW, 1.98892 * 10**30)
    sun.isSun = True

    earth = Planet(-1*Planet.AU, 0, 16, BLUE, 5.9742*10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524*Planet.AU, 0, 12, RED, 6.39*10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(.387*Planet.AU, 0, 9, DARK_GREY, 3.30*10**23)
    mercury.y_vel = -47.4 *1000

    venus = Planet(0.723*Planet.AU, 0, 14, WHITE, 4.8685*10**24)
    venus.y_vel = -35.02 * 1000

    # planets in list so we can loop throuhg and draw
    planets = [sun, earth, mars, mercury, venus]
    # main event loop
    while run:
        clock.tick(60) # fraemrate
        WIN.fill((0,0,0))
        


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN) # loops thru planets and draws each one
        
        pygame.display.update()
    pygame.quit()

main()



