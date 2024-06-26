import pygame

MAX_DAMAGE_TIME = 400
class Character(pygame.sprite.Sprite):

    def __init__(self, size, speed, hp, starting_pos, idle_animation):
        super().__init__()
        # Load and scale player images for walking animation

        scaled_pictures = self.render_image(idle_animation, size)
        # Set up initial image and rect
        self.image = scaled_pictures[0]
        self.rect = self.image.get_rect() #sets the hit box of the sprite
        self.rect.center = starting_pos # Initial the position 

        # Define size and speed attributes
        self.square_size = size
        self.square_speed = speed
        self.hp = hp
        self.taking_damage = 0
        
        # Walking animation attributes
        self.current_animation = scaled_pictures
        self.current_animation_index = 0
        self.current_animation_speed = 100 # Speed of animation change
        self.last_animation_time = pygame.time.get_ticks()
        
    def render_image(self, idle_animation, size):
        loaded_pictures = []
        for pic_name in idle_animation:
            loaded_pictures.append(pygame.image.load(pic_name).convert_alpha())
        scaled_width = size  # New width for the scaled image
        scaled_height = size  # New height for the scaled image

        scaled_pictures = []
        for pic in loaded_pictures:
            scaled_pictures.append(pygame.transform.scale(pic, (scaled_width, scaled_height)))

        return scaled_pictures

    def moveX(self, move):
        self.rect.x += move * self.square_speed
        
    def moveY(self, move):
        self.rect.y += move * self.square_speed

    def getX(self) -> int:
        return self.rect.x

    def getY(self) -> int:
        return self.rect.y
    
    def get_width(self) -> int:
        return self.rect.width

    def get_height(self) -> int:
        return self.rect.height
    
    def get_hp(self) -> int:
        return self.hp
    
    def is_dead(self):
        if(self.hp <= 0):
            self.kill()
            return True

    def take_damage(self, damage):
        self.taking_damage = pygame.time.get_ticks()
        self.hp -= damage
        self.is_dead()

    def get_direction(self):
        return self.direction.get_direction()
        
    def update(self):
        # Update walking animation
        current_time = pygame.time.get_ticks()
        if current_time - self.last_animation_time > self.current_animation_speed:
            self.current_animation_index = (self.current_animation_index + 1) % len(self.current_animation)
            self.image = self.current_animation[self.current_animation_index]
            
            if self.taking_damage + MAX_DAMAGE_TIME > pygame.time.get_ticks():
                red_tint = (255, 0, 0)  # Red color
                tinted_image = self.image.copy()  # Make a copy of the original image
                tinted_image.fill(red_tint, special_flags=pygame.BLEND_MULT)  # Tint the copied image red
                self.image = tinted_image
            
            self.last_animation_time = current_time