import os
import dotenv
import click
from ogsapi.client import OGSClient

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

  print(client.game_details(active_games[selected_game]["id"]))

if __name__ == "__main__":
  cli()
