from json import dumps
import signal
import subprocess
import time
from discordai_modelizer.tests import test_command_line
from discordai_modelizer.tests.conftest import default_file_output
from discordai.template import list_commands
from tests.conftest import TEST_COG_PATH, TEST_COMMAND_NAME


def test_cli_help(script_runner):
    cli = script_runner.run(["discordai", "-h"])
    assert cli.success
    assert "usage: discordai [-h] [-V] {model,job,bot,config} ..." in cli.stdout

    assert "DiscordAI CLI" in cli.stdout
    assert "positional arguments:" in cli.stdout
    assert "{model,job,bot,config}" in cli.stdout
    assert "model               Manage your OpenAI models" in cli.stdout
    assert "job                 Manage your OpenAI jobs" in cli.stdout
    assert "bot                 Manage your Discord bot" in cli.stdout
    assert "config              View your DiscordAI config" in cli.stdout
    assert "option" in cli.stdout
    assert "-h, --help            show this help message and exit" in cli.stdout
    assert "-V, --version         show program's version number and exit" in cli.stdout


def test_cli_model_list(script_runner, init_config):
    test_command_line.test_cli_model_list(script_runner, "discordai")


def test_cli_training(script_runner, init_config, default_file_output):
    test_command_line.test_cli_training(script_runner, "discordai", default_file_output)


def test_cli_model_list_full(script_runner, init_config):
    test_command_line.test_cli_model_list_full(script_runner, "discordai")


def test_cli_delete_model(script_runner, init_config):
    test_command_line.test_cli_delete_model(script_runner, "discordai")


def test_cli_job_list(script_runner, init_config):
    test_command_line.test_cli_job_list(script_runner, "discordai")


def test_job_list_full(script_runner, init_config):
    test_command_line.test_job_list_full(script_runner, "discordai")


def test_job_info(script_runner, init_config):
    test_command_line.test_job_info(script_runner, "discordai")


def test_job_events(script_runner, init_config):
    test_command_line.test_job_events(script_runner, "discordai")


def test_job_cancel(script_runner, init_config):
    test_command_line.test_job_cancel(script_runner, "discordai")


def test_job_cancel(script_runner, init_config):
    test_command_line.test_job_cancel(script_runner, "discordai")


def test_cli_model_bad_args(script_runner, init_config):
    test_command_line.test_cli_model_bad_args(script_runner, "discordai")


def test_cli_job_bad_args(script_runner, init_config):
    test_command_line.test_cli_job_bad_args(script_runner, "discordai")


def test_cli_bot_start(script_runner, init_config):
    proc = subprocess.Popen(
        ["discordai", "bot", "start"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    time.sleep(5)
    proc.send_signal(signal.SIGINT)
    proc.wait()
    stdout, stderr = proc.communicate()

    assert proc.returncode == 0
    for c in list_commands():
        assert f"Loaded extension '{c[1:]}'" in stdout.decode()


def test_cli_list_commands(script_runner, init_config, add_command):
    cli = script_runner.run(["discordai", "bot", "command", "list"])
    assert cli.success
    assert (
        dumps(["/chatgpt", "/imageai", "/test", "/openai", "/customai"], indent=4)
        in cli.stdout
    )


def test_cli_add_commands(script_runner, init_config, remove_command):
    cli = script_runner.run(
        [
            "discordai",
            "bot",
            "command",
            "add",
            "-c",
            f"{TEST_COMMAND_NAME}",
            "-m",
            f"{TEST_COMMAND_NAME}",
        ]
    )
    assert cli.success
    assert TEST_COG_PATH.exists()


def test_cli_delete_commands(script_runner, add_command, reset_command, init_config):
    cli = script_runner.run(
        [
            "discordai",
            "bot",
            "command",
            "delete",
            "-c",
            f"{TEST_COMMAND_NAME}",
            "--force",
        ]
    )
    assert cli.success
    assert not TEST_COG_PATH.exists()


def test_cli_command_bad_args(script_runner, init_config):
    cli = script_runner.run(
        [
            "discordai",
            "bot",
            "command",
        ]
    )
    assert not cli.success
    assert "Must choose a command from `list`, `add`, or `delete`" in cli.stderr


def test_cli_bot_bad_args(script_runner, init_config):
    cli = script_runner.run(
        [
            "discordai",
            "bot",
        ]
    )
    assert not cli.success
    assert "Must choose a command from `start` or `command`" in cli.stderr


def test_cli_fetch_config(script_runner, init_config):
    cli = script_runner.run(
        [
            "discordai",
            "config",
        ]
    )
    assert cli.success
    assert dumps(init_config, indent=4) in cli.stdout


def test_cli_update_config(script_runner, init_config, reset_config):
    cli = script_runner.run(
        [
            "discordai",
            "config",
            "update",
            "DISCORD_BOT_TOKEN",
            "NEW_VALUE",
        ]
    )
    new_conf = init_config
    new_conf["DISCORD_BOT_TOKEN"] = "NEW_VALUE"
    assert cli.success
    assert dumps(new_conf, indent=4) in cli.stdout


def test_cli_update_config_bad_kay(script_runner, init_config):
    cli = script_runner.run(
        [
            "discordai",
            "config",
            "update",
            "BAD_KEY",
            "NEW_VALUE",
        ]
    )
    assert cli.success
    assert "Invalid key provided!" in cli.stdout
