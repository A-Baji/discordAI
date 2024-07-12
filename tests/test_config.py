import os

from io import StringIO
from pytest import fixture
from discordai import config


@fixture(scope="function")
def delete_config():
    (config.config_dir / "config.json").unlink(missing_ok=True)
    yield
    config.get()


def test_get_config(init_config):
    assert init_config == {
        "DISCORD_BOT_TOKEN": f"{os.environ['DISCORD_BOT_TOKEN']}",
        "OPENAI_API_KEY": f"{os.environ['OPENAI_API_KEY']}",
    }


def test_get_config_manual(monkeypatch, delete_config, unset_envs):
    monkeypatch.setattr(
        "sys.stdin", StringIO("TEST_DISCORD_BOT_TOKEN\nTEST_OPENAI_API_KEY\n")
    )
    assert config.get() == {
        "DISCORD_BOT_TOKEN": "TEST_DISCORD_BOT_TOKEN",
        "OPENAI_API_KEY": "TEST_OPENAI_API_KEY",
    }


def test_save_config(reset_config):
    test_config = {
        "DISCORD_BOT_TOKEN": "TEST_DISCORD_BOT_TOKEN",
        "OPENAI_API_KEY": "TEST_OPENAI_API_KEY",
    }
    config.save(test_config)
    assert config.get() == test_config
