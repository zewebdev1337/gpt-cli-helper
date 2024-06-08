import sys
import json
from openai import OpenAI
from dotenv import load_dotenv
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for development environment and binary """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

env_path = resource_path('.env')
load_dotenv(env_path)

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

def load_config():
    default_config_path = resource_path("default_config.json")
    config_path = os.path.expanduser("~/.gpt-cli")
    if not os.path.exists(config_path):
        with open(default_config_path, 'r') as f:
            default_config = json.load(f)
            save_config(default_config)
            return default_config
    with open(config_path, 'r') as f:
        return json.load(f)

def save_config(config):
    config_path = os.path.expanduser("~/.gpt-cli")
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)

def ask_question(model, question, temperature):
    try:
        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            max_tokens=500,
            messages=[
                {"role": "system", "content": "Respond as short as possible. You're cmdline shell assistant. Don't explain unless asked to."},
                {"role": "user", "content": question},
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

def print_help():
    help_text = """
Usage:
    gpt [<model>] <question> [--temp=<TEMP>] [--verbose]    Ask a question
    gpt add_model <MODEL_SHORT_NAME> <MODEL_NAME>           Add new model
    gpt default_model <DEFAULT_MODEL>                       Set default model
    gpt default_temp <TEMP>                                 Set default temperature
    gpt default_verbose                                     Toggle verbose mode
    gpt current_config                                      Show current configuration
    gpt --help                                              Show this message
    [] = optional parameter
"""
    print(help_text)

def main():
    config = load_config()
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    args = sys.argv[1:]
    if "--help" in args:
        print_help()
        sys.exit(0)

    temp_flag = [arg for arg in args if arg.startswith("--temp=")]
    verbose_flag = "--verbose" in args

    temp = config["default_temp"]
    verbose = config["verbose"] or verbose_flag

    if temp_flag:
        temp = float(temp_flag[0].split("=")[1])
        args.remove(temp_flag[0])
    
    if verbose_flag:
        args.remove("--verbose")

    if args[0] == "default_model":
        config['default_model'] = args[1]
        save_config(config)
        print(f"Default model set to {args[1]}")
    elif args[0] == "default_temp":
        config["default_temp"] = float(args[1])
        save_config(config)
        print(f"Default temperature set to {args[1]}")
    elif args[0] == "default_verbose":
        config["verbose"] = not config["verbose"]
        save_config(config)
        status = "enabled" if config["verbose"] else "disabled"
        print(f"Verbose mode {status}")
    elif args[0] == "add_model":
        config['models'][args[1]] = args[2]
        save_config(config)
        print(f"Model {args[1]} added as {args[2]}")
    elif args[0] == "current_config":
        print(json.dumps(config, indent=4))
    else:
        if args[0] in config['models']:
            model = config['models'][args[0]]
            question = " ".join(args[1:])
        else:
            model = config['models'][config['default_model']]
            question = " ".join(args)

        if verbose:
            print(f"Model: {model}, Temperature: {temp}")

        answer = ask_question(model, question, temp)
        if answer:
            print(answer)

if __name__ == "__main__":
    main()
