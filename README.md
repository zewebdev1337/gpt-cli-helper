# GPT Command Line Helper

Ever forget a command's name, syntax or options and just want to get it done quickly without [RTFM](https://en.wikipedia.org/wiki/RTFM) or even whipping out a browser? Ask GPT from your CLI!

## Installation

```bash
git clone git@github.com:zewebdev1337/gpt-cli-helper.git
cd gpt-cli-helper
chmod +x install.sh
sudo ./install.sh
```

The `install.sh` script will perform the following actions:

1. Create and activate virtual python environment.
2. Install pip dependencies.
3. Use PyInstaller to create a standalone executable.
4. Move the executable to `/usr/local/bin/` for easy access.
5. Clean up the build and venv directories.

## Requirements

- Python 3.6 or higher
- OpenAI API Key

## Usage

After installation, you can use the `gpt` command to ask questions.

Example:

```bash
$ gpt exit from active python venv?
deactivate
$ gpt format in github markdown for a link?
`[link text](URL)`
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
