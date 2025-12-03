# HonseTrans
a silly script for using a LLM to translate silly honse game\
*(i dont even know how to code)*

## Usage
This repo works best when paired with an lm studio server
### Config
The following Scripts require a config.toml file with parameters (as an example):
```
api_url = "http://127.0.0.1:1234/v1/chat/completions"
api_key = "key"
model = "model_name"
temperature = 0.1
max_tokens = 3000
top_p = 0.95
top_k = 40
repetition_penalty = 1.1
```

### Story/Home Files
Use UmaTL Tools to extract files from the game and place in the raw folder\
It should use a similar format to the "example.json" file\
**run ```py main.py```**\
*These files need to be converted back into hachimi format once done being translated*

### Character System Text
Find a way to extract the character system text from the game in hachimi format and place it in the root directory with file name "character_system_text.json". Can also add an already existing "character_system_text_dict.json" where the script will avoid duplicate translations and append the new translations to it.\
**run ```py translate_character_system.py```**

### Post Cleaning Scripts
Names should be self explanatory but are mainly specific to the model and dictionary I have on my setup
