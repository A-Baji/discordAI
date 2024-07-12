from io import StringIO
import os
from pathlib import Path
import appdirs
from pytest import fixture
from discordai import template
from .conftest import TEST_COMMAND_NAME, TEST_COG_PATH


def test_list_commands(add_command):
    commands = template.list_commands()
    for c in commands:
        assert c in [
            "/chatgpt",
            "/imageai",
            f"/{TEST_COMMAND_NAME}",
            "/openai",
            "/customai",
        ]


def test_add_command(add_command):
    assert TEST_COG_PATH.exists()


def test_delete_command(add_command, reset_command):
    template.delete_command(command_name=f"{TEST_COMMAND_NAME}", force=True)
    assert not TEST_COG_PATH.exists()


def test_delete_command_cancel(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", StringIO("N\n"))
    template.delete_command(command_name=f"{TEST_COMMAND_NAME}")
    stdout = capsys.readouterr()
    assert "Cancelling command deletion..." in stdout.out


def test_delete_command_fail(capsys):
    template.delete_command(command_name="BAD_NAME", force=True)
    stdout = capsys.readouterr()
    assert (
        "Failed to delete command: No command with that name was found." in stdout.out
    )


def test_get_cogs_path():
    assert (
        template.get_cogs_path()
        == Path(os.path.dirname(template.__file__)) / "bot" / "cogs"
    )


def test_get_cogs_path_frozen(run_as_frozen):
    assert (
        template.get_cogs_path()
        == Path(appdirs.user_data_dir(appname="discordai"))
        / "discordai"
        / "bot"
        / "cogs"
    )
