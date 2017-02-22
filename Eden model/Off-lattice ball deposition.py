import pygame
import random
import math
import time

'''TODO: fix the particles_frozen mechanic such that it works correctly i.e. find a way to make it collide but not calculate any of the Newtonian mechanic things'''
'''TODO: in roughness(), implement the roughness calculation for each row, and deleting the row afterwards.'''

# Ask about viva tips - how to prepare the best? Structure of the presentation etc, time allocation for each section etc.
    # 15 mins, no more than 15 slides, story, doesnt have to be everything we done, some of the work, methods. Save q&a for "tried but didn't work stuff"
    # focus on stuff that worked, include graphs, make sure that labels are large, font large
# Ask about poster, are there any sample ones to look at
# Ask about report: structure and how many words on each section etc. (and can we use lit review as basis without self-plagiarising?)
# Are there any previous reports we can take a look at

background_colour = (255, 255, 255)
(width, height) = (800, 800)
mass_of_air = 0
gravity = (math.pi, 0.01)

# just loop things
counter = 0
pause = 0

global_time = 0

my_particles_frozen = []
particle_row = []

results = []

elasticity = 0.2    # 0 means balls stick i.e. what percentage of speed is retained on bounce


def addVectors((angle1, length1), (angle2, length2)):
    '''
    Mathematical function to add vectors together
    :return:
    '''
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2

    angle = 0.5 * math.pi - math.atan2(y, x)
    length = math.hypot(x, y)

    return (angle, length)


def findParticle(particles, x, y):
    '''
    Find particles of different sizes
    :param particles:
    :param x:
    :param y:
    :return:
    '''
    for p in particles:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p
    return None


def newParticle():
    '''
    Picks random size, density, speed etc.
    :return:
    '''
    size = random.randint(10, 20)
    density = random.randint(1, 20)
    x = random.randint(size, width - size)
    y = random.randint(size, size+1)

    particle = Particle((x, y), size, density * size ** 2)
    particle.colour = (200 - density * 10, 200 - density * 10, 255)
    particle.speed = random.random()
    particle.angle = random.uniform(0, math.pi * 2)

    my_particles.append(particle)


def newParticleRow():
    '''
    Instantiates a row of new particles which are the same size as the average size of the particles (so they theoretically fit nicely on top of the row)
    :return:
    '''
    size = 15
    density = 1
    y = 1
    dummy = 0

    for x in range(width):
        dummy = dummy + 1
        if dummy % 30 == 0:
            particle = Particle((x, y), size, density * size ** 2)
            # particle.colour = (200 - density * 10, 200 - density * 10, 255)
            particle.speed = 0
            particle.angle = 0

            particle.colour = (0, 255, 255)

            my_particles.append(particle)

            particle_row.append(particle)


def roughness(particleRow_array):
    '''

    :param particleRow_array:
    :return:
    '''

    coord_list = []

    for i, particle in enumerate(particleRow_array):

        coord_list.append(particle.y_coord())

        # perform the roughness calculation and calculate alpha for this timestep

        alpha = 1 + 1

        results.append((alpha, global_time))

        # delete the whole particle row

    '''TODO: roughness calculation using an array of particle IDs as input i.e. finish this function off'''

    return


def collide(p1, p2):
    '''
    Collision mechanics between two particles
    :param p1:
    :param p2:
    :return:
    '''
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size:
        tangent = math.atan2(dy, dx)
        angle = 0.5 * math.pi + tangent

        angle1 = 2 * tangent - p1.angle
        angle2 = 2 * tangent - p2.angle
        speed1 = p2.speed * elasticity
        speed2 = p1.speed * elasticity

        (p1.angle, p1.speed) = (angle1, speed1)
        (p2.angle, p2.speed) = (angle2, speed2)

        p1.x += math.sin(angle)
        p1.y -= math.cos(angle)
        p2.x -= math.sin(angle)
        p2.y += math.cos(angle)


class Particle:
    '''
    Particle class
    '''

    def __init__(self, (x, y), size, mass=1):
        self.particle_frozen = 0  # 0 for off

        self.x = x
        self.y = y
        self.size = size
        self.colour = (102, 0, 255)    # a beautiful purple
        self.thickness = 0
        self.speed = 0
        self.angle = 0
        self.mass = mass
        #self.drag = (self.mass/(self.mass + mass_of_air)) ** self.size

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def freeze(self):
        self.particle_frozen = 1

    def unfreeze(self):
        self.particle_frozen = 0

    def x_coord(self):
        return self.x

    def y_coord(self):
        return self.y

    def move(self):
        (self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        #self.speed *= self.drag

    def bounce(self):
        if self.x > width - self.size:
            self.x = 2*(width - self.size) - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        if self.y > height - self.size:
            self.y = 2*(height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Eden deposition off-lattice')

number_of_particles = 40
my_particles = []

for n in range(number_of_particles):
    newParticle()

selected_particle = None
running = True

while running:

    global_time = global_time + 1

    counter = counter + 1

    '''Every x timesteps a new particle falls'''
    if counter % 50 == 0 and pause == 0:
        newParticle()

    '''Every y timesteps measure the roughness by depositing a row of particles and calculating using their x, y positions. After they have fallen freeze all particles so it takes up less computing time'''

    if counter == 2000:
        pause = 1

    if counter == 3000:
        newParticleRow()

    if counter == 4000:
        '''TODO: probably under here goes the calculating the roughness and the deleting the particle row'''
        for i, particle in enumerate(my_particles):
            particle.freeze()
        counter = 0
        pause = 0

        roughness(particle_row)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     (mouseX, mouseY) = pygame.mouse.get_pos()
        #     selected_particle = findParticle(my_particles, mouseX, mouseY)
        # elif event.type == pygame.MOUSEBUTTONUP:
        #     selected_particle = None

    # if selected_particle:
    #     (mouseX, mouseY) = pygame.mouse.get_pos()
    #     dx = mouseX - selected_particle.x
    #     dy = mouseY - selected_particle.y
    #     selected_particle.angle = 0.5*math.pi + math.atan2(dy, dx)
    #     selected_particle.speed = math.hypot(dx, dy) * 0.1

    screen.fill(background_colour)

    '''Loop over all particles and calculate mechanics etc'''

    for i, particle in enumerate(my_particles):
        if my_particles[i].particle_frozen == 0:
            particle.move()
            particle.bounce()
        for particle2 in my_particles[i+1:]:
            collide(particle, particle2)
        particle.display()

    pygame.display.flip()
