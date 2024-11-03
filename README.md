# Not Finished & A Work In Progress

An open source [Discord](https://discord.com/) bot written in Python that allows users on servers to play mini-games and get awarded points! So far, there is only a questionnaire game in development, but more games will be added in the future!

**NOTE** - As stated before, this bot is not finished and unusable in its current state. I'm pushing to this repository for transparency with the project and I also want to save to the cloud.

## Command Line Usage
The following flags are supported in the command line.

| Name | Flags | Default | Description |
| ---- | ----- | ------- | ----------- |
| CFG Path | `-c --cfg` | `./conf.json` | The path to the JSON Config file. |
| List | `-l --list` | N/A | Lists all values from config. |
| Help | `-h --help` | N/A | Prints the help menu. |

## Stats & Database
*To Do...*

## Configuration
The default config file is located at `./conf.json`.

| Name | Key | Type | Default | Description |
| ---- | --- | ---- | ------- | ----------- |
| Debug | `debug` | Debug Object | `{}` | The debug object. |
| General | `general` | General Object | `{}` | The general object. |
| Discord Bot | `bot` | Discord Bot Object | `{}` | The Discord bot object. |
| Connections | `connections` | Connections Object | `{}` | The connections object. |
| Servers | `servers` | Servers Object | `{}` | The servers object. |

### Debug Object
The debug object contains settings on debugging.

| Name | Key | Type | Default | Description |
| ---- | --- | ---- | ------- | ----------- |
| Verbose Level | `verbose` | int | `1` | The verbose level for debugging. |
| Log To File | `log_to_file` | bool | `false` | Whether to log to a file. |
| Log Directory | `log_dir` | string | `./logs` | The logs directory. |

### General Object
The general object contains general settings for the project.

| Name | Key | Type | Default | Description |
| ---- | --- | ---- | ------- | ----------- |

*To Do...*

### Discord Bot Object
The Discord Bot object contains settings related to the Discord bot.

| Name | Key | Type | Default | Description |
| ---- | --- | ---- | ------- | ----------- |
| Token | `token` | string | `""` | The bot token. |

### Connections Object
The connections object contains settings related to the web API and database connections. These settings aren't required, but having both disabled will disable stats.

| Name | Key | Type | Default | Description |
| ---- | --- | ---- | ------- | ----------- |
| Web API | `api` | Web API Object | `{}` | The web API object. |
| Database | `db` | Database Object | `{}` | The database object. |

#### Web API Object
The web API object contains settings on the web API for the web back-end.

| Name | Key | Type | Default | Description |
| ---- | --- | ---- | ------- | ----------- |
| Enabled | `enabled` | bool | `false` | Whether to enable the web API. |
| Host | `host` | string | `"http://localhost"` | The web host (port may be included). |
| Token | `token` | string | None | The authorization token passed with each web request. |
| Web Config | `web_config` | bool | `true` | Whether to pull configuration from the web API when enabled. |

#### Database Object
The database object contains settings on the **PostgreSQL** database.

| Name | Key | Type | Default | Description |
| ---- | --- | ---- | ------- | ----------- |
| Enabled | `enabled` | bool | `false` | Whether to enable the database. |
| Host | `host` | string | `"localhost"` | The database host. |
| Port | `port` | int | `5432` | The database port. |
| Username | `user` | string | `"root"` | The database user. |
| Password | `password` | string | `""` | The database password. |
| Web Config | `web_config` | bool | `true` | Whether to pull configuration from the database when enabled. |

### Servers Object
The server's object contains server-specific settings including what games to run, its settings, and more!

The object contains sub-objects where the key (string) is the server GUID (you may retrieve this through Discord if you have the proper permissions to the server).

The value is another object with these settings.

| Name | Key | Type | Default | Description |
| ---- | --- | ---- | ------- | ----------- |
| Next Game Random | `next_game_random` | bool | `true` | Whether to pick a random next game. |
| Next Game Cooldown | `next_game_cooldown` | float | `120.0` | The cooldown between starting a new game when automatically starting a game. |
| Game Start Auto | `game_start_auto` | bool | `true` | Whether to start games automatically. |
| Game Start Command | `game_start_cmd` | bool | `true` | Whether to allow starting a game through a command. |
| Game Start Manual | `game_start_manual` | bool | `true` | Whether to allow starting a specific game manually by passing an argument to the start command. |

There is also a `games` object that is used for determining what games should be enabled for the server and the games settings. Sub objects inside of the `games` object should contain a key with the game's module name (the file names excluding `.py` in [`src/game`](./src/game), ex: `questionnaire`). The sub-object's value should be another object containing additional settings. Check the config example for more information!

## Web Back-End
While the bot's configuration can be handled locally inside of the JSON config file, you may also setup the bot's web back-end which comes with an authentication system and also allows users to sign in through Discord, invite the bot to their Discord server, and then configure it to their needs.

*Not Finished...*

## Running
Firstly, make sure you configure the project. I recommend copying the [`conf_ex.json`](./conf_ex.json) to `./conf.json`.

You may then use Python to run the program. You must run this project with Python version 3 or higher.

Here are some examples.

```bash
# Run bot with no arguments.
python3 src/main.py

# Set config file to /etc/discord-mg.json
python3 src/main.py -c /etc/discord-mg.json

# List all config values.
python3 src/main.py -l

## Print help menu.
python3 src/main.py -h
```

### Running With Docker
*To Do...*

## Credits
* [Christian Deacon](https://github.com/gamemann)