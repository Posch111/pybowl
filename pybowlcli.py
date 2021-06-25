# Command line interface for the bowling game.
import click
from pybowl import BowlingGame, Player

def start_bowling(players):
    # game = BowlingGame(players)
    game = BowlingGame(players, autoplay=True)
    game.start()

@click.command('Bowling Game')
@click.option('--names', prompt='Enter the name of each player separated by a comma (max 4)', help='Enter the name of each player separated by a comma. Example: {__file__} Larry, Bonnie, Phillip')
@click.option('--autoplay', help='Plays the game automatically for you.')
def get_players(names, autoplay):
    print(autoplay)
    if len(names) > 100:
        print('Too many characters input (max: 100). Exiting...')
        exit()
    
    names = [n.strip() for n in names.split(',')]
    if len(names) > 4:
        print('Only 4 players allowed. Exiting...')
        exit()
    if len(names) == 0:
        print('No players. Exiting...')
        exit()

    print('Players entered: ', ', '.join(names))

    players = []
    id = 0
    for name in names:
        players.append(Player(name, id))
        id += 1

    start_bowling(players)

if __name__ == '__main__':
    get_players()