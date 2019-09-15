from Pokemon import *
from MainApp import *
from Player import *

# global variables
VERSION = '2.8.0'
ROOT = os.path.dirname(os.path.realpath(__file__))
COMMON = os.path.join(ROOT, 'media', 'Common')
IMG_PKMN_DIR = os.path.join(ROOT, 'media', 'pokemon')
PLAYER_DIR = os.path.join(ROOT, 'players')
DATA = os.path.join(ROOT, 'data')

def init_player_information():
    # create player directory
    if not os.path.isdir(PLAYER_DIR):
        os.mkdir(PLAYER_DIR)
    if not os.listdir(PLAYER_DIR):
        with open(os.path.join(PLAYER_DIR, 'Virgo.csv'), 'w', encoding='utf-8', newline='') as file:
            pass
    # get Pokemon information
    for filename in os.listdir(PLAYER_DIR):
        if filename.endswith('.csv'):
            with open(os.path.join(PLAYER_DIR, filename), 'r', encoding='utf-8') as file:
                player_name = os.path.splitext(os.path.basename(file.name))[0]
                reader = csv.reader(file)
                # get trainer portrait info
                portrait = int(next(reader)[0]) if os.stat(os.path.join(PLAYER_DIR, filename)).st_size != 0 else random.randint(0, 91)
                temp_pkmn_list = []
                for row in reader:
                    if row:
                        temp_pkmn_list.append(Pokemon(row))
                PLAYERS.append(Player(player_name, portrait, temp_pkmn_list))
                playerNames.append(player_name)


if __name__ == '__main__':
    # before starting the GUI, gather player information
    init_player_information()
    app = MainApp()

    # disable resizing of window
    app.resizable(False, False)

    # set the title of the windows
    app.title('Rentals v%s' %VERSION)
    app.mainloop()
