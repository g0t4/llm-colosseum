git clone https://github.com/g0t4/llm-colosseum
# fork of https://github.com/OpenGenerativeAI/llm-colosseum
# open README.md
#   says follow install docs:
#   https://docs.diambra.ai/#installation
#     register an account
#
cd llm-colosseum
veinit # (use 3.11) => makes diambra CLI avail too
  python3.11 -m venv --clear --upgrade-deps .venv && source .venv*/bin/activate.fish && pip3 install -r requirements.txt

diambra arena list-roms # compatible roms
  # COMPATIBLE SHAS listed
  # sfiii3n https://github.com/g0t4/llm-colosseum/blob/main/eval/game.py#L216

# google / download it
sha256sum sfiii3n.zip # verify SHA
mkdir ~/.diambra/roms
mv ~/Downloads/sfiii3n.zip ~/.diambra/roms/

# start deps:
# start docker
ollama serve # update to latest
ollama pull qwen:14b-chat-v1.5-fp16 # PRE PULL models (see ollama_entry.py to change models)


make local # => ollama_entry.py (uses ollama)
  # login to account on diambra site
  # * creates token in ~/.diambra/credentials
  # OR for OpenAI/Grok/etc use:
    make run
    cp .env.example .env # API KEYS here... https://github.com/OpenGenerativeAI/llm-colosseum/blob/4452871e38031562ea673b20cc3b49425fffd46c/.env.example#L5
      # FYI I do not like API keys in files in a repo at all...

# python 3.12 failed so I switched to 3.11
#   AND I renamed ollama.py to ollama_entry.py - was colliding with ollama package:
#     from ollama import Client, AsyncClient
#     ImportError: cannot import name 'Client' from 'ollama'

# FYI see commit history for how I rewrote logging to make it easier to see what is going on w/ LLM responses and actual moves
