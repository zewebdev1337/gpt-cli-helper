import sys
import json
from openai import OpenAI
from dotenv import load_dotenv
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import google.generativeai as genai
import anthropic

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

anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')
mistral_api_key = os.getenv('MISTRAL_API_KEY')
codestral_api_key = os.getenv('CODESTRAL_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')

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

def ask_question(model, question, temperature, system_message, max_tokens):
    try:
        if model.startswith("claude"):
            client = anthropic.Client(api_key=anthropic_api_key)
            response = client.messages.create(
                messages=[
                    ChatMessage(role="user", content=f"{anthropic.HUMAN_PROMPT} {question}{anthropic.AI_PROMPT}"),
                ],
                system=system_message,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.content[0].text
            # returns [TextBlock(text='Hello.', type='text')]. how do I extract text?
        elif model.startswith("gemini"):
            genai.configure(api_key=google_api_key)
            model = genai.GenerativeModel(model_name=model)
            chat = model.start_chat(history=[])
            response = chat.send_message(question)
            return response.text
        elif model.startswith("open-mi") or model.startswith("mistral"):
            client = MistralClient(api_key=mistral_api_key)
            response = client.chat(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                messages=[
                    ChatMessage(role="system", content=system_message),
                    ChatMessage(role="user", content=question),
                ]
            )
            return response.choices[0].message.content
        elif model.startswith("codestral"):
            client = MistralClient(api_key=codestral_api_key, endpoint="https://codestral.mistral.ai/v1/chat/completions")
            response = client.chat(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                messages=[
                    ChatMessage(role="system", content=system_message),
                    ChatMessage(role="user", content=question),
                ]
            )
            return response.choices[0].message.content
        elif model.startswith("gpt-"):
            client = OpenAI(api_key=openai_api_key)
            response = client.chat.completions.create(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": question},
                ]
            )
            return response.choices[0].message.content
        else:
            return f"Unsupported model: {model}"
    except Exception as e:
        return f"An error occurred: {e}"


def print_help():
    help_text = """
Usage:
    gpt [<model>] <question> [--temp=<TEMP>] [--system=<SYSTEM_MESSAGE>] [--verbose] [--max_tokens=<MAX_TOKENS>]
    gpt add_model <MODEL_SHORT_NAME> <MODEL_NAME>           Add new model
    gpt default_model <DEFAULT_MODEL>                       Set default model
    gpt default_temp <TEMP>                                 Set default temperature
    gpt default_system_message <SYSTEM_MESSAGE>             Set default system message
    gpt default_max_tokens <MAX_TOKENS>                     Set default max tokens
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
    system_flag = [arg for arg in args if arg.startswith("--system=")]
    max_tokens_flag = [arg for arg in args if arg.startswith("--max_tokens=")]
    verbose_flag = "--verbose" in args

    temp = config["default_temp"]
    system_message = config["default_system_message"]
    max_tokens = config["default_max_tokens"]
    verbose = config["verbose"] or verbose_flag

    if temp_flag:
        temp = float(temp_flag[0].split("=")[1])
        args.remove(temp_flag[0])
    
    if system_flag:
        system_message = system_flag[0].split("=", 1)[1]
        args.remove(system_flag[0])   

    if max_tokens_flag:
        max_tokens = max_tokens_flag[0].split("=", 1)[1]
        args.remove(max_tokens_flag[0])

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
    elif args[0] == "default_max_tokens":
        config["default_max_tokens"] = int(args[1])
        save_config(config)
        print(f"Default max tokens set to {args[1]}")
    elif args[0] == "default_system_message":
        config["default_system_message"] = args[1]
        save_config(config)
        print(f"Default system message set to: {args[1]}")
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
            print(f"Model: {model}, Temperature: {temp}, System Message: {system_message}, Max Tokens: {max_tokens}")

        answer = ask_question(model, question, temp, system_message, max_tokens)
        if answer:
            print(answer)

if __name__ == "__main__":
    main()