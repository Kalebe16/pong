from pyglet.font import add_file as load_font
from pyglet.media import load as load_sound

# Fonts
load_font('../assets/fonts/press_start_2p.ttf')
font_press_start_2p = 'Press Start 2P'

# Sounds
sound_click = load_sound('../assets/sounds/click.wav', streaming=False)
sound_you_win = load_sound('../assets/sounds/you_win.wav', streaming=False)
sound_tuc = load_sound('../assets/sounds/tuc.wav', streaming=False)
