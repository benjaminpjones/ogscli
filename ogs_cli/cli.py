import os
import dotenv
import click
from ogsapi.client import OGSClient
from .go_utils import Baduk, Coordinate

dotenv.load_dotenv()
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

def get(client, endpoint):
  return client.api.call_rest_endpoint('GET', endpoint=endpoint).json()

@click.command()
@click.option('--username', prompt=True, help='Your OGS username')
@click.password_option(confirmation_prompt=False)
def cli(username: str, password: str):
  if CLIENT_ID is None:
     print("Warning: CLIENT_ID not set.")

  client = OGSClient(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    username=username,
    password=password,
    log_level="ERROR"
  )

  active_games = get(client, endpoint="/ui/overview")["active_games"]
  for i, game in enumerate(active_games):
    print(f'{i+1}) {game["id"]} - {game["name"]} - {game["black"]["username"]} v. {game["white"]["username"]}')

  selected_game = int(input("select a game:")) - 1

  game_details = client.game_details(active_games[selected_game]["id"])
  moves = game_details["gamedata"]["moves"]
  b = Baduk(game_details["width"], game_details["height"])
  for move in moves:
    b.play_move(Coordinate(move[0], move[1]))
  print(b)



if __name__ == "__main__":
  cli()
