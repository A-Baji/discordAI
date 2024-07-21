# Changelog

Observes [Semantic Versioning](https://semver.org/spec/v2.0.0.html) standard and [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) convention.

## [3.1.0] - 07-21-2024

### Added

- support for the new gpt4o mini model in gpt commands and made it the default model

## [3.0.2] - 07-16-2024

### Fixed

- bug where custom slash commands would return error due to emoji map issues

## [3.0.1] - 07-16-2024

### Changed

- updated modelizer to version [3.0.11](https://github.com/A-Baji/discordAI-modelizer/releases/tag/3.0.11)
- slash command error output is more descriptive

### Fixed

- log downloading for non linux operating systems
- bug where empty prompts would print "**" when bold was true


## [3.0.0] - 07-12-2024

### Added

- support for python 3.12
- unit tests

### Changed

- updated modelizer to version [3.0.9](https://github.com/A-Baji/discordAI-modelizer/releases/tag/3.0.9)
- updated and pinned openai to version 1.35.5
  -  includes various updates to the included slash commands
- updated DiscordChatExporter to version 2.43.3
- refactor/optimization/general cleanup of code
- improved dev environment
- updated some cli args
- updated some cli help strings
- updated config handling

### Removed

- support for python 3.8
- token usage tracking for /chatgpt command

## [2.0.1] - 06-15-2023

### Changed

- updated documentation
- updated modelizer to version [2.0.0](https://github.com/A-Baji/discordAI-modelizer/releases/tag/2.0.1)

## [2.0.0] - 06-15-2023

### Added

- a changelog
- an OpenAI image generation command
- the gpt3.5 model to the openai command and made it the default
- a chatGPT command with chat history functionality
- custom emoji support for custom models.

### Fixed

- upgrading the packaged executable version now properly applies any new features to existing, non-custom cogs
- bug where two stars would appear for blank prompts for custom model completions

### Changed

- made prompt bolding for custom model completions a Discord command parameter
- updated modelizer to version [2.0.0](https://github.com/A-Baji/discordAI-modelizer/releases/tag/2.0.0)

## [1.3.2] - 02-22-2023

### Changed

- updated modelizer to version [1.2.2](https://github.com/A-Baji/discordAI-modelizer/releases/tag/1.2.2)

## [1.3.1] - 02-19-2023

### Changed

- updated modelizer to version [1.2.1](https://github.com/A-Baji/discordAI-modelizer/releases/tag/1.2.1)

## [1.3.0] - 02-17-2023

### Added

- CLI option to bolden the prompt for custom model completions
- CLI option to set the thought time
- CLI option to set the min and max thought length
- CLI option to only output the events for the job status

### Changed

- updated modelizer to version [1.2.0](https://github.com/A-Baji/discordAI-modelizer/releases/tag/1.2.0)

## [1.2.1] - 02-12-2023

### Added

- option to provide a different openai key to the customai command

## [1.2.0] - 02-11-2023

### Changed

- updated modelizer to version [1.1.0](https://github.com/A-Baji/discordAI-modelizer/releases/tag/1.1.0)

## [1.1.1] - 02-11-2023

### Added

- pinned modelizer to version [1.1.0](https://github.com/A-Baji/discordAI-modelizer/releases/tag/1.0.1)

### Changed

- switched from using `os.path` to `pathlib`

## [1.1.0] - 01-29-2023

### Changed

- modified readme

[3.1.0]: https://github.com/A-Baji/discordAI/compare/3.0.2...3.1.0
[3.0.2]: https://github.com/A-Baji/discordAI/compare/3.0.1...3.0.2
[3.0.1]: https://github.com/A-Baji/discordAI/compare/3.0.0...3.0.1
[3.0.0]: https://github.com/A-Baji/discordAI/compare/2.0.1...3.0.0
[2.0.1]: https://github.com/A-Baji/discordAI/compare/1.3.2...2.0.1
[2.0.0]: https://github.com/A-Baji/discordAI/compare/1.3.2...2.0.0
[1.3.2]: https://github.com/A-Baji/discordAI/compare/1.3.1...1.3.2
[1.3.1]: https://github.com/A-Baji/discordAI/compare/1.3.0...1.3.1
[1.3.0]: https://github.com/A-Baji/discordAI/compare/1.2.1...1.3.0
[1.2.1]: https://github.com/A-Baji/discordAI/compare/1.2.0...1.2.1
[1.2.0]: https://github.com/A-Baji/discordAI/compare/1.1.1...1.2.0
[1.1.1]: https://github.com/A-Baji/discordAI/compare/1.1.0...1.1.1
[1.1.0]: https://github.com/A-Baji/discordAI/compare/1.0.0...1.1.0