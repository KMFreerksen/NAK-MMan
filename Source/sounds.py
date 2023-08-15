import pygame


class Sounds:
    def __init__(self):
        self.intro = pygame.mixer.Sound("sounds/pacman_beginning.wav")
        self.chomp = pygame.mixer.Sound("sounds/pacman_chomp.wav")
        self.eat_ghost = pygame.mixer.Sound("sounds/pacman_eatghost.wav")
        self.extra_life = pygame.mixer.Sound("sounds/pacman_extrapac.wav")
        self.eat_fruit = pygame.mixer.Sound("sounds/pacman_eatfruit.wav")
        self.pacman_dies = pygame.mixer.Sound("sounds/pacman_death.wav")

    def play_intro(self):
        pygame.mixer.Sound.play(self.intro)

    def play_pacman_eating(self):
        pygame.mixer.Sound.play(self.chomp)

    def play_eat_ghost(self):
        pygame.mixer.Sound.play(self.eat_ghost)

    def play_extra_life(self):
        pygame.mixer.Sound.play(self.extra_life)

    def play_eat_fruit(self):
        pygame.mixer.Sound.play(self.eat_fruit)

    def play_pacman_dies(self):
        pygame.mixer.Sound.play(self.pacman_dies)


def play_sound(sound_file):
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
    except pygame.error:
        print(f"Error: Cannot play the sound file {sound_file}")


def play_pacman_intro():  # Working in code
    sound_file = "pacman_beginning.wav"
    play_sound(sound_file)


def play_pacman_eating():  # Working in code
    sound_file = "pacman_chomp.wav"
    play_sound(sound_file)


def play_pacman_eat_ghost():
    sound_file = "pacman_eat-ghost.wav"
    play_sound(sound_file)


def play_pacman_extra_life():
    sound_file = "pacman_extract.wav"
    play_sound(sound_file)


def play_pacman_eat_fruit():
    sound_file = "pacman_eatfruit.wav"
    play_sound(sound_file)


def play_pacman_dies():  # Working in code
    sound_file = "pacman_death.wav"
    play_sound(sound_file)


if __name__ == "__main__":
    # Example usage:
    #play_pacman_intro()
    #play_pacman_eating()
    #play_pacman_eat_ghost()
    #play_pacman_extra_life()
    play_pacman_eat_fruit()
    #play_pacman_dies()
