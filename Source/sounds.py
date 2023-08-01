import pygame


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
    sound_file = "sounds/pacman_beginning.wav"
    play_sound(sound_file)


def play_pacman_eating():  # Working in code
    sound_file = "sounds/pacman_chomp.wav"
    play_sound(sound_file)


def play_pacman_eat_ghost():
    sound_file = "sounds/pacman_eat-ghost.wav"
    play_sound(sound_file)


def play_pacman_extra_life():
    sound_file = "sounds/pacman_extract.wav"
    play_sound(sound_file)


def play_pacman_eat_fruit():
    sound_file = "sounds/pacman_eat fruit.wav"
    play_sound(sound_file)


def play_pacman_dies():  # Working in code
    sound_file = "sounds/pacman_death.wav"
    play_sound(sound_file)


if __name__ == "__main__":
    # Example usage:
    play_pacman_intro()
    play_pacman_eating()
    play_pacman_eat_ghost()
    play_pacman_extra_life()
    play_pacman_eat_fruit()
    play_pacman_dies()
