import pygame, sys
from random import randint, uniform

class Ship(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('./assets/graphics/ship.png').convert_alpha()
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.mask = pygame.mask.from_surface(self.image)
        self.can_shoot = True
        self.shoot_time = None
        self.laser_sound = pygame.mixer.Sound('./assets/sounds/laser.ogg')

    def input_position(self):
        self.rect.center = pygame.mouse.get_pos()

    def meteor_collision(self):
        if pygame.sprite.spritecollide(self, meteor_group, True, pygame.sprite.collide_mask):
            pygame.quit()
            sys.exit()
    def laser_shoot(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            Laser(laser_group, self.rect.midtop)
            self.laser_sound.play()

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > 500:
                self.can_shoot = True

    def update(self):
        self.input_position()
        self.laser_timer()
        self.laser_shoot()
        self.meteor_collision()

class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)
        self.image = pygame.image.load('./assets/graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)

        self.mask = pygame.mask.from_surface(self.image)

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0, -1)
        self.speed = 600
        self.explosion_sound = pygame.mixer.Sound('./assets/sounds/explosion.wav')

    def meteor_collision(self):
        if pygame.sprite.spritecollide(self, meteor_group, True, pygame.sprite.collide_mask):
            self.kill()
            self.explosion_sound.play()
    def update(self):
        self.pos += self.speed * self.direction * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        if self.rect.bottom < 0:
            self.kill()

        self.meteor_collision()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)
        self.meteor_surf = pygame.image.load('./assets/graphics/meteor.png').convert_alpha()
        self.meteor_size = pygame.math.Vector2(self.meteor_surf.get_size()) * uniform(0.5, 1.5)
        self.scaled_surf = pygame.transform.scale(
            self.meteor_surf,
            self.meteor_size
        )
        self.image = self.scaled_surf
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 600)

        self.rotation = 0
        self.rotation_speed = randint(20, 50)

    def rotate(self):
        self.rotation += self.rotation_speed * dt
        rotated_surf = pygame.transform.rotozoom(self.scaled_surf, self.rotation, 1)
        self.image = rotated_surf
        self.rect = self.image.get_rect(center = self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        self.pos += self.speed * self.direction * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        if self.rect.top > WINDOW_HEIGHT:
            self.kill()

        self.rotate()

class Score:
    def __init__(self):
        self.font = pygame.font.Font('./assets/graphics/subatomic.ttf')

    def display(self):
        score_text = f'Score: {pygame.time.get_ticks() // 1000}'
        text_surf = self.font.render(score_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80))
        display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(display_surface, (255, 255, 255), text_rect.inflate(30, 30), width = 8, border_radius = 5)

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption('Space Shooter')

clock = pygame.time.Clock()

background_surf = pygame.image.load('./assets/graphics/background.png').convert()

spaceship_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()

ship = Ship(spaceship_group)

meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 400)

score = Score()

bg_music = pygame.mixer.Sound('./assets/sounds/music.wav')
bg_music.play(loops = -1)

#game loop
while True:

    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == meteor_timer:
            meteor_y_pos = randint(-150, -50)
            meteor_x_pos = randint(-100, WINDOW_WIDTH + 100)
            Meteor(meteor_group, (meteor_x_pos, meteor_y_pos))

    #delta
    dt = clock.tick(120) / 1000

    #update
    spaceship_group.update()
    laser_group.update()
    meteor_group.update()

    #graphics
    display_surface.blit(background_surf, (0, 0))

    score.display()
    spaceship_group.draw(display_surface)
    laser_group.draw(display_surface)
    meteor_group.draw(display_surface)


    #draw frame
    pygame.display.update()

