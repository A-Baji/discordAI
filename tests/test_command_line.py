from json import dumps
from discordai_modelizer.tests import test_command_line
from discordai_modelizer.tests.conftest import default_file_output


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
