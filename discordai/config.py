import os
import pathlib
import json
import appdirs

config_dir = pathlib.Path(appdirs.user_data_dir(appname="discordai"))


def get():
    config_path = config_dir / "config.json"
    if config_path.exists():
        with open(config_path, "r") as file:
            config = json.load(file)
            os.environ["DISCORD_BOT_TOKEN"] = config["DISCORD_BOT_TOKEN"]
            os.environ["OPENAI_API_KEY"] = config["OPENAI_API_KEY"]
    else:
        token = os.getenv("DISCORD_BOT_TOKEN")
        openai_key = os.getenv("OPENAI_API_KEY")
        if not (token and openai_key):
            print("No config found. Please follow the steps to create one:")
        else:
            print("Creating config from env:")
        if token:
            print(f"Set DISCORD_BOT_TOKEN value to {token}")
        if openai_key:
            print(f"Set OPENAI_API_KEY value to {openai_key}")

        config = dict(
            DISCORD_BOT_TOKEN=token or input("\nEnter your Discord bot token: "),
            OPENAI_API_KEY=openai_key or input("\nEnter your OpenAI key: "),
        )
        os.environ["DISCORD_BOT_TOKEN"] = config["DISCORD_BOT_TOKEN"]
        os.environ["OPENAI_API_KEY"] = config["OPENAI_API_KEY"]
        save(config)
        print(f"Your config has been saved to {config_dir / 'config.json'}")

    return config


def save(config):
    os.makedirs(config_dir, exist_ok=True)
    with open(pathlib.Path(config_dir, "config.json"), "w") as f:
        f.write(json.dumps(config))
