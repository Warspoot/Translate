import json
import requests
import toml
import time

# Load dictionary
with open("dictionary.json", "r", encoding="utf-8") as file:
    dictionary = json.load(file)
    dictionary_json_str = json.dumps(dictionary, ensure_ascii=False)

# Load config
with open("config.toml", "r") as f:
    config = toml.load(f)

# Load existing translations to avoid duplicates
try:
    with open("character_system_text_dict.json", "r", encoding="utf-8") as file:
        existing_translations = json.load(file)
    print("Loaded existing translations from character_system_text_dict.json")
except FileNotFoundError:
    print("No existing translations found, starting fresh")
    existing_translations = {}

def translate(rawText):
    api_key = config["server"]["api_key"]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    post_request = {
        "model": config["server"]["model"],
        "temperature": config["server"]["temperature"],
        "messages": [
            {
                "role": "system",
                "content": f"{config['server']['system_prompt']} Refer to below for a dictionary in json format with the order japanese_text : english_text. (example\"ミホノブルボン\": \"Mihono Bourbon\", which means translate ミホノブルボン to Mihono Bourbon. \n {dictionary_json_str} \n translate the below text",
            },
            {
                "role": "user", "content": rawText
            }
        ],
    }

    optional_params = {
        "top_p": config["server"]["top_p"],
        "top_k": config["server"]["top_k"],
        "max_tokens": config["server"]["max_tokens"],
        "repetition_penalty": config["server"]["repetition_penalty"]
    }

    for param, value in optional_params.items():
        if value is not None:
            post_request[param] = value

    response = requests.post(
        config["server"]["api_url"],
        headers=headers,
        json=post_request
    )
    json_traslated = response.json()
    trans_text = json_traslated["choices"][0]["message"]["content"]
    print(f"Translation: {trans_text}")
    return trans_text

def process_character_system_text():
    print("Loading character_system_text.json")
    file_start_time = time.time()

    with open("character_system_text.json", "r", encoding="utf-8") as file:
        char_data = json.load(file)

    total_processed = 0
    total_skipped = 0
    total_translated = 0

    combined_translations = existing_translations.copy()

    for char_id, char_texts in char_data.items():
        print(f"\n=== Processing Character ID: {char_id} ===")

        # Ensure this character ID exists in combined translations
        if char_id not in combined_translations:
            combined_translations[char_id] = {}

        if char_id in existing_translations:
            existing_char = existing_translations[char_id]
        else:
            existing_char = {}

        for text_id, jp_text in char_texts.items():
            total_processed += 1

            if text_id in existing_char:
                print(f"  Text ID {text_id} (SKIP): Already translated in dict")
                total_skipped += 1
                continue

            if not jp_text or not jp_text.strip():
                print(f"  Text ID {text_id} (SKIP): Empty text")
                total_skipped += 1
                continue

            print(f"  Text ID {text_id}: {jp_text}")
            en_text = translate(jp_text)
            en_text = en_text.replace('\n', ' ').replace('  ', ' ').replace("\n### Response:\n", "").strip()

            combined_translations[char_id][text_id] = en_text
            print(f"  Translated: {en_text}")
            total_translated += 1

    with open("character_system_text_dict.json", "w", encoding="utf-8") as file:
        json.dump(combined_translations, file, indent=4, ensure_ascii=False)

    file_end_time = time.time()
    file_duration = file_end_time - file_start_time

    print(f"\n{'='*50}")
    print(f"Translation complete!")
    print(f"Total entries processed: {total_processed}")
    print(f"Skipped (already in dict): {total_skipped}")
    print(f"Newly translated: {total_translated}")
    print(f"Saved combined translations to character_system_text_dict.json")
    print(f"Total time: {file_duration:.2f} seconds.")
    print(f"{'='*50}")

if __name__ == "__main__":
    process_character_system_text()
