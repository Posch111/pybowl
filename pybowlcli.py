# Command line interface for the bowling game.
import click
from pybowl import BowlingGame, Bowler

def start_bowling(bowlers, autoplay):
    BowlingGame(bowlers, autoplay).start()

@click.command()
@click.option('--player_names', required=True, prompt='Enter the name of each player separated by a comma (max 4)', help=f'Enter the name of each player separated by a comma. Example: Larry, Bonnie, Phillip')
@click.option('-ap', '--autoplay', help='Plays the game automatically for you.', is_flag=True)
def get_players(player_names, autoplay):
    if len(player_names) > 100:
        print('Too many characters input (max: 100). Exiting...')
        exit()
    
    player_names = [n.strip() for n in player_names.split(',')]
    if len(player_names) > 4:
        print('Only 4 players allowed. Exiting...')
        exit()
    if len(player_names) == 0:
        print('No players. Exiting...')
        exit()

    print('Players entered: ', ', '.join(player_names))

    bowlers = []
    id = 0
    for name in player_names:
        bowlers.append(Bowler(name, id))
        id += 1

    start_bowling(bowlers, autoplay)

if __name__ == '__main__':
    get_players()