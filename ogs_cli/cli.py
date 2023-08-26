import os
import dotenv
import click
from ogsapi.client import OGSClient

dotenv.load_dotenv()
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')


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


if __name__ == "__main__":
  cli()
