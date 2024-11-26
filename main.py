import pygame, sys

class Ship(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('./assets/graphics/ship.png').convert_alpha()
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.can_shoot = True
        self.shoot_time = None

    def input_position(self):
        self.rect.center = pygame.mouse.get_pos()

    def laser_shoot(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            print('shoot laser')
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > 500:
                self.can_shoot = True

    def update(self):
        self.input_position()
        self.laser_timer()
        self.laser_shoot()

class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)
        self.image = pygame.image.load('./assets/graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0, -1)
        self.speed = 600

    def update(self):
        self.pos += self.speed * self.direction * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption('Space Shooter')

clock = pygame.time.Clock()

background_surf = pygame.image.load('./assets/graphics/background.png').convert_alpha()

spaceship_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()

ship = Ship(spaceship_group)
laser = Laser(laser_group, (100, 300))

#game loop
while True:

    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #delta
    dt = clock.tick(120) / 1000

    #update
    spaceship_group.update()
    laser_group.update()

    #graphics
    display_surface.blit(background_surf, (0, 0))
    spaceship_group.draw(display_surface)
    laser_group.draw(display_surface)


    #draw frame
    pygame.display.update()

