# DiscordAI
DiscordAI is CLI package that you can use to run your discord bot. You can create customized openAI models based on a discord channel and user, and then add new slash commands to your bot to use these custom models to create openAI completions.

## Installation
### Executable
Download the CLI executable for your OS from the [latest release](https://github.com/A-Baji/discordAI/releases/latest). Unfortunately, the Mac version of the executable is not available due to stability issues.
### Pip
`pip install -U git+https://github.com/A-Baji/discordAI.git`
#### Or
1. Download/clone the source locally
2. Run `pip install -U <path to source>/.`
3. The source may now be deleted

## Usage Guide
This is a step by step guide on how to use discordAI.
### Set up a discord bot
The first step to get started with discordAI is to create a discord bot. A good guide for this can be found [here](https://discordpy.readthedocs.io/en/stable/discord.html#creating-a-bot-account). Once you've created the bot you need to enable `MESSAGE CONTENT INTENT` to allow your bot to read chat messages. This can be done by following [this guide](https://umod.org/community/discord/40519-how-to-enable-message-content-intent). Finally, discord bots only have access to channels they are members of, so invite your bot to the server you want to use by following [this guide](https://discordpy.readthedocs.io/en/stable/discord.html#inviting-your-bot). The only scope you need to select is `bot`, and no permissions are required. Make sure to save your bot's token somewhere safe, as it will be needed the first time you run discordAI.
### Create a OpenAI account
Next, head over to openAI's [signup page](https://beta.openai.com/signup) and get an [API key](https://beta.openai.com/account/api-keys). A free openAI API key comes with $18 of credit. This is important as the main usage of discordAI requires openAI credits. You can view your credit usage at any time by going to your [openAI account page](https://beta.openai.com/account/usage). Again, Make sure to save your openAI API key somewhere safe, as it will be needed the first time you run discordAI.
### Create a new customized openAI model
Now that you have your own discord bot token and openAI API key, you can start using discordAI. First run `discordai bot start --sync` to initialize your bot. You will be asked for your bot token and API key, which will be saved for future use. These values can be changed at any time using the [config commands](https://github.com/A-Baji/discordAI#Config).

The model creation process can be broken down into three steps: downloading the logs of a specified channel, parsing the logs into an openAI-compatible dataset, and then training an openAI model using that dataset.

Pick a channel and user that you want to use for your custom model and run `discordai model create -c <channel_id> -u "<username#id>" --dirty`. You can follow [this guide](https://turbofuture.com/internet/Discord-Channel-ID) to learn how to get a channel's ID. Make sure that you include the full username with the #id, and wrap it in quotes if it contains spaces. The `--dirty` flag prevents the outputted dataset files from being deleted. Downloaded chat logs get saved and reused, but you can set the `--redownload` flag if you want to update the logs.

You may have noticed the lack of a model customization process occurring after running that command. This is because no base model was selected, but before you specify a base model, you should analyze the generated dataset located in the directory mentioned in the logs. Chat messages are parsed into a dataset by grouping individual messages sent within a certain timeframe into "thoughts", where each thought is a completion in the dataset. The default for this timeframe is 10 seconds. If your dataset looks a bit off, try different timeframe settings using the `-t` option: 
`discordai model create -c <channel_id> -u "<username#id>" -t <timeframe> --dirty`

After you've found a good timeframe setting, you will want to manage your dataset's size. The larger your dataset is, the more openAI credits it will cost to create a custom model. By default, the max dataset size is set to 1000. If your dataset exceeds this limit, it will be reduced using either a "first", "last", "middle", or "even" reduction method. The "first" method will select the first n messages, "last" will select the last n, "middle" will select the middle n, and "even" will select an even distribution of n messages. The default reduction mode is even. You can set the max dataset size and reduction mode using the `-m` and `-r` options: 
`discordai model create -c <channel_id> -u "<username#id>" -t <timeframe> -m <max_size> -r <reduction_mode> --dirty`

If you are planning on creating multiple models, you may want to get your hands on multiple openAI API keys in order to maximize the free credit usage. You can assign specific api keys to custom models using the `-o` option. Otherwise, the key provided in your config will be used.

Now that you have fine tuned your dataset, you can finally begin the customization process by specifying a base model. OpenAI has four base [models](https://beta.openai.com/docs/models/gpt-3): davinci, curie, babbage, and ada, in order of most advanced to least advanced. Generally you will want to use davinci, but it is also the most expensive model as well as the longest to customize. Select your base model with the `-b` option.

Your final command should look something like this: 
`discordai model create -c <channel_id> -u "<username#id>" -t <timeframe> -m <max_size> -r <reduction_mode> -b <base_model>`
### Test the new model
After the customization process is complete, it's time test your new model to figure out the best settings for it. Grab the model id provided in the logs of the customization process, or use `discordai model list --simple` to get a list of your model ids. Start up your bot with `discordai bot start` and head over to a discord channel that your bot is in. For starters, try entering `/customai model:<model_id> promp:<test_prompt>` and see what you get. 

Typically, models complete prompts by answering them. For example, if you ask the davinci model "What color is the sky?", it might reply with "The sky is blue.". However, since the prompts of our dataset were all empty, our models will complete prompts by continuing them rather than answering. So if you provide the prompt "The sky is the color" to your custom model, it might reply "The sky is the color blue". If you were to ask your custom model a question as a prompt like in the first example, it would continue the prompt as if it were the one who asked the question.

With this understanding of how prompts work, you will want to try out different values for the other options of the `/customai` command in order to figure out what the best settings are for your model. A description of each option is listed when you type the command, but for more information you can visit openAI's [documentation](https://beta.openai.com/docs/api-reference/completions).
### Create a new slash command for the model
Once you've found the best settings for your model, you can create a new slash command for your discord bot that will use your model by default: `discordai bot commands new -n <command_name> -i <model_id> -t <temp_default> -p <pres_default> -f <freq_default> -m <max_tokens_default>`

The options after `-n` and `-i` are to set the *defaults* for the slash command. Alternate values can be used when calling the command in discord, just like how `/openai` and `/customai` work. If your model was created using a different openAI API key from the one in your config, you will have to specify it using the `-o` option.

Slash commands can be updated at any time by calling `discordai bot commands new` with the same <command_name> but different default values. You can also delete slash commands with `discordai bot commands delete -n <command_name>`.

After creating a new slash command, remember to sync your slash commands with discord's servers by running `discordai bot start --sync`, or by using `@bot_name sync global` in discord.

### Questions
If you have any questions, feel free to make a new post in [discussions](https://github.com/A-Baji/discordAI/discussions/categories/q-a). If you encounter any issues while using discordAI, make sure to create a new [issue](https://github.com/A-Baji/discordAI/issues).

## Commands
### Bot
Commands related to your discord bot
#### `discordai bot start`
Start your discord bot
#### `discordai bot commands`
Manage your discord bot's slash commands
* `discordai bot commands new`
  * Create a new slash command for your bot that will use a customized model for completions
* `discordai bot commands delete`
  * Delete a slash command from your bot
#### `@bot_name sync|unsyc guild|global`
These are special non-CLI commands that must be run *in discord*, in a channel that your bot is a member of. They are used to update or remove your bot's slash commands from discord's servers.
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