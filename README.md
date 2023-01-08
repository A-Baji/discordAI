# DiscordAI

DiscordAI is CLI package that you can use to run your discord bot. It can also be used to create customized openAI models based on a discord channel and user. The bot comes with two slash commands that use openAI's API to create prompt completions. There are also two hidden commands that are used to synchronize your bot's commands with discord: `@bot_name sync|unsyc guild|global`.

## Installation
### Executable
Download the CLI executable for your OS from the [latest release](https://github.com/A-Baji/discordAI/releases/latest). Unfortunately, the Mac version of the executable is not available due to stability issues.
### Pip
`pip install -U git+https://github.com/A-Baji/discordAI.git`
#### Or
1. Download/clone the source locally
2. Run `pip install -U <path to source>/.`
3. The source may now be deleted

## Commands
### Bot
Commands related to your discord bot
#### `discordai bot start`
Start your bot
#### `discordai bot commands`
Manage slash commands
* `discordai bot commands new`
  * Create a new slash command by filling out a template
* `discordai bot commands delete`
  * Delete a slash command
### Model
Commands related to your openAI models
#### `discordai model list`
List your openAi customized models
#### `discordai model create`
Create a new openAI customized model by downloading the specified chat logs, parsing them into a usable dataset, and then training a customized model using openai
#### `discordai model delete`
Delete an openAI customized model
### Job
Commands related to your openAI jobs
#### `discordai job list`
List your openAI customization jobs
#### `discordai job follow`
Follow an openAI customization job
#### `discordai job status`
Get an openAI customization job's status
#### `discordai job cancel`
Cancel an openAI customization job
### Config
View and modify your config
#### `discordai config bot-token`
Get or set your discord bot token
#### `discordai job openai-key`
Get or set your openaAI API key

## Disclaimer
This application allows users to download the chat history of any channel for which they have permission to invite a bot, and then use those logs to create an openai model based on a user's chat messages. It is important to note that this application should only be used with the consent of all members of the channel. Using this application for malicious purposes, such as impersonation, or without the consent of all members is strictly prohibited.

By using this application, you agree to use it responsibly. The developers of this application are not responsible for any improper use of the application or any consequences resulting from such use. We strongly discourage using this application for any unethical purposes.