# DiscordAI
DiscordAI is a CLI driver program for Discord bots. You can create fine-tuned OpenAI models based on a Discord channel and user, and then add new slash commands for your Discord bot to use these fine-tuned models in OpenAI completions.

DiscordAI is a parent module of [DiscordAI Modelizer](https://github.com/A-Baji/DiscordAI-modelizer).

## Installation
### Executable
Download the CLI executable for your OS from the [latest release](https://github.com/A-Baji/DiscordAI/releases/latest). Unfortunately, the Mac version of the executable is not available due to stability issues.

### Pip
`pip install -U git+https://github.com/A-Baji/DiscordAI.git`

#### Or
1. Download/clone the source locally
2. Run `pip install -U <path to source>/.`
3. The source may now be deleted

## Usage Guide
This is a step-by-step guide on how to use DiscordAI.

### Create an OpenAI account
The first step to get started with DiscordAI is to head over to OpenAI's [signup page](https://platform.openai.com/signup) and get an [API key](https://platform.openai.com/api-keys) and store it somewhere safe. Unfortunately, fine-tuning with OpenAI now requires **paid credits**. This is important as the main usage of DiscordAI requires OpenAI credits. To add credits to your OpenAI account, go to [the billing page](https://platform.openai.com/settings/organization/billing/payment-methods). Once you add a credit card to your account, credits will automatically be purchased as needed according to your payment settings. You can add credit [usage limits](https://platform.openai.com/settings/organization/limits) to further control this. You can view your credit usage at any time by going to your [usage page](https://platform.openai.com/organization/usage). Again, make sure to save your OpenAI API key somewhere safe, as it will be needed the first time you run DiscordAI.

### Set up a Discord bot
Next, you'll need to create a Discord bot. A good guide for this can be found [here](https://discordpy.readthedocs.io/en/stable/discord.html#creating-a-bot-account). Once you've created the bot you need to enable `MESSAGE CONTENT INTENT` to allow your bot to read chat messages. This can be done by following [this guide](https://umod.org/community/discord/40519-how-to-enable-message-content-intent). Finally, Discord bots only have access to channels they are members of, so invite your bot to the server you want to use by following [this guide](https://discordpy.readthedocs.io/en/stable/discord.html#inviting-your-bot). The only scope you need to select is `bot`, and no permissions are required. Make sure to save your bot's token somewhere safe, as it will be needed the first time you run DiscordAI.

### Create a new fine-tuned OpenAI model
Now that you have your own Discord bot token and OpenAI API key, you can start using DiscordAI. First, run `discordai bot start --sync` to initialize your bot. You will be asked for your Discord bot token and OpenAI API key, which will be saved locally for future use. These values can be changed at any time using the [config commands](https://github.com/A-Baji/DiscordAI#Config).

The model creation process can be broken down into three steps: downloading the logs of a specified channel, parsing the logs into an OpenAI-compatible dataset, and then training an OpenAI model using that dataset.

#### Generate a dataset with default parameters
Pick a channel and user whose chat logs you want to use for creating your fine-tuned model and run:

`discordai model create -c <channel_id> -u <username> --dirty`

You can follow [this guide](https://turbofuture.com/internet/Discord-Channel-ID) to learn how to find a Discord channel's ID. The `--dirty` flag prevents the outputted dataset files from being automatically deleted for cleanup. Downloaded chat logs get saved and reused, but you can use the `--redownload` flag if you want to update the logs.

#### Calibrate the "thought" building parameters
The next step is to analyze the generated dataset located in the directory mentioned in the logs. Chat messages are parsed into a dataset by grouping individual messages sent within a certain timeframe into "thoughts", where each thought is a completion in the dataset. The default for this timeframe is 5 seconds. The length of each thought must also be within the minimum and maximum thought length. The default minimum is 6 words and the default maximum is `None`, or optional. You want the completions in your dataset to look as close as possible to complete sentences. If your dataset looks a bit off, try different settings using the `--ttime`, `--tmin`, and `--tmax` options:

`discordai model create -c <channel_id> -u <username> --ttime <timeframe> --tmax <thought_max> --tmin <thought_min> --dirty`

#### Set the max line count
After you've found good thought settings, you will want to manage your dataset's size. The larger your dataset, the more OpenAI credits it will cost to create a fine-tuned model. The dataset size can be controlled with the `-m` option with a default of 1000, meaning the dataset will be 1000 lines long:

`discordai model create -c <channel_id> -u <username> --ttime <timeframe> --tmax <thought_max> --tmin <thought_min> -m <max_size> --dirty`

#### Choose how lines are selected
The lines in a dataset are selected sequentially by default. You can use the `--distributed` flag to evenly space out the selected lines. For example, if a dataset is 12 lines long but the maximum is set to 4, lines 1-4 will be selected. However, in distributed mode, every 3rd line will be selected. Furthermore, you can offset the starting point of your dataset using the `--os` option and reverse the selection order using the `--reverse` flag. Keep in mind that selection gets reversed before being offset:

`discordai model create -c <channel_id> -u <username> --ttime <timeframe> --tmax <thought_max> --tmin <thought_min> -m <max_size> --os <offset> --distributed --reverse --dirty`

#### Manually edit the dataset if needed
If you are still not satisfied with the resulting dataset, you can manually alter it and then use the `--use_existing` flag. This will skip the dataset processing step and instead use the pre-existing dataset. Make sure not to change the name of the dataset file:

`discordai model create -c <channel_id> -u <username> --ttime <timeframe> --tmax <thought_max> --tmin <thought_min> -m <max_size> --os <offset> --distributed --reverse --use_existing --dirty`

#### Select a base model
Now that you have adjusted your dataset, you can finally begin the fine-tuning process by specifying a base model. OpenAI has two base models available for fine-tuning: `davinci` and `babbage`. Babbage is a less advanced, cheaper model that may be used for testing purposes. Select your base model with the `-b` option.

Your final command should look something like this:

`discordai model create -c <channel_id> -u <username> --ttime <timeframe> --tmax <thought_max> --tmin <thought_min> -m <max_size> --os <offset> --distributed --reverse --use_existing -b <base_model>`

You can track the fine-tuning progress on your [OpenAI dashboard](https://platform.openai.com/finetune).

### Test the new model
After the fine-tuning process is complete, it's time to test your new model to figure out the best settings for it.

#### Using OpenAI's playground
Model testing can be done conveniently through [OpenAI's playground](https://platform.openai.com/playground/complete). Select your model from the dropdown on the right, write out a test prompt, and then click "submit". For best results, start your prompt with `"<username> says: "`, (using the username of the user that the model was trained on) since the prompts in the training dataset follow the same pattern. Prompts should be the start of a sentence so that the model may complete them. You'll want to try out various prompts and parameters until you find settings for `Temperature`, `Frequency penalty`, and `Presence penalty` that work the best. Avoid altering the `Top P` parameter.

#### Using /customai
Alternatively, you can use the `/customai` Discord command which comes with DiscordAI. Copy the model id provided in the logs of the fine-tuning process, or use `discordai model list` to get a list of your models. Start up your bot with `discordai bot start` and head over to a Discord channel that your bot is in. From here you can use the same process as you would in OpenAI's playground but instead using `/customai model:<model_id> prompt:<test_prompt>`. In this case, using the `"<username> says: "` format is not necessary as it is automatically added in the back-end.

### Create a new slash command for the model
Once you have found the most suitable values for the `Temperature`, `Frequency penalty`, and `Presence penalty` parameters, you can create a new slash command for your Discord bot which will use the new fine-tuned model with those settings:

`discordai bot command add -c <command_name> -m <model_id> -t <temp_default> -p <pres_default> -f <freq_default> -m <max_tokens_default>`

The options after `-c` and `-m` are to set the *defaults* when using the slash command. Alternate values can be used when calling the command in Discord, just like how `/openai` and `/customai` work.

Slash commands can be updated at any time by calling `discordai bot command add` with the same <command_name> and the new desired default values. You can also delete slash commands with `discordai bot command delete -c <command_name>`.

After creating a new slash command, remember to sync your slash commands with Discord's servers by running `discordai bot start --sync`, or by using `@<your_bot> sync global` in Discord. See the [commands description](https://github.com/A-Baji/discordAI?tab=readme-ov-file#your_bot-syncunsync-guildglobal) for more about syncing your bot.

### Questions
If you have any questions, feel free to make a new post in [discussions](https://github.com/A-Baji/DiscordAI/discussions/categories/q-a). If you encounter any issues while using DiscordAI, make sure to create a new [issue](https://github.com/A-Baji/DiscordAI/issues).

## Commands
### Bot
Commands related to your Discord bot
#### `discordai bot start`
Start your Discord bot
#### `discordai bot command`
Manage your Discord bot's slash commands
* `discordai bot command list`
  * List all slash commands for your bot
* `discordai bot command add`
  * Create a new slash command for your bot that will use a fine-tuned model for completions
* `discordai bot command delete`
  * Delete a slash command from your bot
#### `@<your_bot> sync|unsync guild|global`
These are special non-CLI commands that must be run *in Discord*, in a channel that your bot is a member of. They are used to update or remove your bot's slash commands from Discord's servers.

### Model
Commands related to your OpenAI models
#### `discordai model list`
List your OpenAI fine-tuned models
#### `discordai model create`
Create a new OpenAI fine-tuned model by downloading the specified chat logs, parsing them into a usable dataset, and then training a fine-tuned model using OpenAI
#### `discordai model delete`
Delete an OpenAI fine-tuned model

### Job
Commands related to your OpenAI jobs
#### `discordai job list`
List your OpenAI fine-tuning jobs
#### `discordai job info`
Get an OpenAI fine-tuning job's info
#### `discordai job events`
Get an OpenAI fine-tuning job's events
#### `discordai job cancel`
Cancel an OpenAI fine-tuning job

### Config
Commands related to your config
#### `discordai config`
View your config and its local path
#### `discordai config update key value`
Update the value of a config key: `DISCORD_BOT_TOKEN` | `OPENAI_API_KEY`

## Disclaimer
This application allows users to download the chat history of any channel for which they have permission to invite a bot, and then use those logs to create an OpenAI model based on a user's chat messages. It is important to note that this application should only be used with the consent of all members of the channel. Using this application for malicious purposes, such as impersonation, or without the consent of all members is strictly prohibited.

By using this application, you agree to use it responsibly. The developers of this application are not responsible for any improper use of the application or any consequences resulting from such use. We strongly discourage using this application for any unethical purposes.

This application is not affiliated with or endorsed by Discord, Inc. The use of the term "Discord" in our product name is solely for descriptive purposes to indicate compatibility with the Discord platform.
