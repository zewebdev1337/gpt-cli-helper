#!/bin/bash
# install.sh

if [ ! -f .env ]; then
  read -p "Enter your Anthropic API key: " anthropic_api_key
  read -p "Enter your Google API key: " google_api_key
  read -p "Enter your Mistral API key: " mistral_api_key
  read -p "Enter your Codestral API key: " codestral_api_key
  read -p "Enter your OpenAI API key: " openai_api_key
  echo "ANTHROPIC_API_KEY=${anthropic_api_key}" > .env
  echo "GOOGLE_API_KEY=${google_api_key}" >> .env
  echo "MISTRAL_API_KEY=${mistral_api_key}" >> .env
  echo "CODESTRAL_API_KEY=${codestral_api_key}" >> .env
  echo "OPENAI_API_KEY=${openai_api_key}" > .env
fi

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

pyinstaller --onefile --add-data '.env:.' --add-data 'default_config.json:.' gpt.py
mv dist/gpt /usr/local/bin/
deactivate
rm -rf build/ dist/ .venv/ gpt.spec .env