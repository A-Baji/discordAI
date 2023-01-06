# DiscordAI

DiscordAI is CLI package that you can use to run your discord bot. It can also be used to create customized openAI models based on a discord channel and user. The bot comes with two slash commands that use openAI's API to create prompt completions. There are also two hidden commands that are used to synchronize your bot's commands with discord: `@bot_name sync|unsyc guild|global`.

## Installation
### Executable
Download the CLI executable from the [latest release](https://github.com/A-Baji/discordAI/releases/latest)
### Pip
`pip install -U git+https://github.com/A-Baji/discordAI.git`
#### Or
1. Download/clone the source locally
2. Run `pip install -U <path to source>/.`
3. The source may now be deleted

## Commands
### `discordai start`
This command will start your bot
### `discordai openai create`
This command will download the specified chat logs, parse them into a usable dataset, then create a customized model using openai.
### `discordai openai list_jobs`
This command will list all of your openai customization jobs.
### `discordai openai list_models`
This command will list all of your openai customized models.
### `discordai openai follow`
This command will output the event stream of a specified customization job process.
### `discordai openai status`
This command will output the status of a specified customization job.
### `discordai openai cancel`
This command will cancel a specified customization job.
### `discordai openai delete`
This command will delete a specified customized model.

## Disclaimer
This application allows users to download the chat history of any channel for which they have permission to invite a bot, and then use those logs to create an openai model based on a user's chat messages. It is important to note that this application should only be used with the consent of all members of the channel. Using this application for malicious purposes, such as impersonation, or without the consent of all members is strictly prohibited.

By using this application, you agree to use it responsibly. The developers of this application are not responsible for any improper use of the application or any consequences resulting from such use. We strongly discourage using this application for any unethical purposes.