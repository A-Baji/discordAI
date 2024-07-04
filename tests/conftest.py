import os
from shutil import rmtree
import sys
import appdirs

from pytest import fixture
from pathlib import PosixPath, Path
from discordai import template, config

TEST_COMMAND_NAME = "test"
TEST_COG_PATH = template.get_cogs_path() / f"{TEST_COMMAND_NAME}.py"
PY_VER = ".".join(os.environ["PYTHON_VERSION"].split(".")[:2])


@fixture(scope="function")
def run_as_frozen():
    setattr(sys, "frozen", True)
    setattr(
        sys,
        "_MEIPASS",
        PosixPath(f"/usr/local/lib/python{PY_VER}/site-packages"),
    )
    yield
    cogs_data_dir = Path(appdirs.user_data_dir(appname="discordai")) / "discordai"
    if cogs_data_dir.exists():
        rmtree(cogs_data_dir)
    delattr(sys, "_MEIPASS")
    setattr(sys, "frozen", False)


@fixture(scope="session")
def init_config():
    yield config.get()
    (config.config_dir / "config.json").unlink(missing_ok=True)


@fixture(scope="function")
def unset_envs():
    DISCORD_BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
    del os.environ["DISCORD_BOT_TOKEN"]
    del os.environ["OPENAI_API_KEY"]
    yield
    os.environ["DISCORD_BOT_TOKEN"] = DISCORD_BOT_TOKEN
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
