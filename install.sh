#!/bin/bash

if [ ! -f .env ]; then
  read -p "Enter your GPT API key: " api_key
  echo "OPENAI_API_KEY=${api_key}" > .env
fi

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

pyinstaller --onefile --add-data '.env:.' gpt.py
mv dist/gpt /usr/local/bin/
deactivate
rm -rf build/ dist/ .venv/
