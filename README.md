# GPT Command Line Helper

Ever forget a command's name, syntax, or options and just want to get it done quickly without [RTFM](https://en.wikipedia.org/wiki/RTFM) or even whipping out a browser? Ask GPT from your CLI!

## Installation

```bash
git clone git@github.com:zewebdev1337/gpt-cli-helper.git
cd gpt-cli-helper
chmod +x install.sh
sudo ./install.sh
```

The `install.sh` script will perform the following actions:

1. Create and activate a virtual Python environment.
2. Install pip dependencies.
3. Use PyInstaller to create a standalone executable.
4. Move the executable to `/usr/local/bin/` for easy access.
5. Clean up the build and venv directories.

## Requirements

- Python 3.6 or higher
- OpenAI API Key

## Usage

After installation, you can use the `gpt` command to ask questions.
## Commands

- **Basic command:**

  ```bash
  gpt <question>
  ```

  Example:
  ```bash
  $ gpt format in github markdown for a link?
  `[link text](URL)`
  ```

- **Ask a Question:**
  ```bash
  gpt [<model>] <question> [--temp=<TEMP>] [--verbose]
  ```

  Default models: `3.5, 4, 4-turbo, 4o`

  Example:
  ```bash
  $ gpt 3.5 How to change directory in Linux?
  cd <directory_name>
  ```
  **NOTICE:**
  
  If your question contains quotes, be sure to wrap it with another type of quote, otherwise it will mess up with the syntax and return an error.

  Example:
  ```bash
  $ gpt "what's the command to list all files in cd"
  ls
  $ gpt 'say "hello, world!" in Japanese'
  こんにちは世界!
  ```

- **Add Model:**
  ```bash
  gpt add_model <MODEL_SHORT_NAME> <MODEL_NAME>
  ```
  Example:
  ```bash
  $ gpt add_model 4-turbo-preview gpt-4-turbo-preview
  ```

- **Set Default Model:**
  ```bash
  gpt default_model <DEFAULT_MODEL>
  ```
  Example:
  ```bash
  $ gpt default_model 4-turbo-preview
  ```

- **Set Default Temperature:**
  ```bash
  gpt default_temp <TEMP>
  ```
  Example:
  ```bash
  $ gpt default_temp 0.5
  ```

- **Toggle Verbose Mode:**
  ```bash
  gpt default_verbose
  ```
  Example:
  ```bash
  $ gpt default_verbose
  Verbose mode enabled
  ```
  Example output with verbose mode:
  ```bash
  $ gpt exit from active python venv?
  Model: gpt-4o, Temperature: 0
  deactivate
  ```

- **Show Current Config:**
  ```bash
  gpt current_config
  ```
  Example output:
  ```bash
  $ gpt current_config
  {
      "default_model": "4o",
      "default_temp": 0,
      "verbose": false,
      "models": {
          "3.5": "gpt-3.5-turbo",
          "4": "gpt-4",
          "4-turbo": "gpt-4-turbo",
          "4o": "gpt-4o"
      }
  }
  ```

## Configuration

### Configuration file location

The configuration file is located at `~/.gpt-cli`

### Configuration options

Starting from v2.0 you can configure several options:

- **Default Model:** Change the default model used.
- **Default Temperature:** Change the default temperature for responses.
- **Verbose Mode:** Enable or disable verbose mode.
- **Add Model:** Add a new model to the model list.

### Default settings
  - **Default model:** `gpt-4o`
  - **Default temperature:** `0`
  - **Verbose mode:** `Disabled`
  - **Available models:**
    - `gpt-3.5-turbo`
    - `gpt-4`
    - `gpt-4-turbo`
    - `gpt-4o`

### Modify defaults

Modify `default_config.json` before running the install script.

## Compatibility

The tool is designed for Linux and support for other OSes is not planned. 
If you want support for other OS, please fork or mirror the repo. 

PRs and issues regarding support for other OSes will be closed as `Will not implement`

## License

This project is licensed under the MIT License - see the LICENSE file for details.
