import os
import pathlib
import json
import appdirs

config_dir =  pathlib.Path(appdirs.user_data_dir(appname="discordai"))


def get():
    try:
        with open(config_dir / "config.json", 'r') as file:
            config = json.load(file)
    except FileNotFoundError as err:
        print("No config found. Please follow the steps to create one:")
        config = dict(
            token=os.getenv("DISCORD_TOKEN") or input("\nEnter your discord bot token: "),
            openai_key=os.getenv("OPENAI_KEY") or input("\nEnter your openAI key: ")
        )
        os.makedirs(config_dir, exist_ok=True)
        with open(pathlib.Path(config_dir, "config.json"), "w") as f:
            f.write(json.dumps(config))

        print(f"Your config has been saved to {config_dir / 'config.json'}")
    return config


def save(config):
    os.makedirs(config_dir, exist_ok=True)
    with open(pathlib.Path(config_dir, "config.json"), "w") as f:
        f.write(config)
