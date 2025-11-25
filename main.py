import json
import requests
import toml
import os

target_folder = "raw"

with open("dictionary.json", "r", encoding="utf-8") as file:
    dictionary = json.load(file)
    dictionary_json_str = json.dumps(dictionary, ensure_ascii = False)

with open("config.toml", "r") as f:
    config = toml.load(f)

def process_json(file_path):
    print(f"Loading {file_path}")
    count = -1
    with open(file_path, "r", encoding="utf-8") as file:
        raw_load = json.load(file)

    while True:
        count = count + 1
        try:
            print("Name: ",raw_load["text"][count]["jpName"])
            enName = translate(raw_load["text"][count]["jpName"])
            if enName == "Monologue":
                enName = " "
            raw_load["text"][count]["enName"] = enName

            print("Text: ",raw_load["text"][count]["jpText"])
            enText = translate(raw_load["text"][count]["jpText"])
            raw_load["text"][count]["enText"] = enText
        except IndexError: 
            print("Finished!")
            break
        try:
            print("Choice: ",raw_load["text"][count]["choices"][0]["jpText"])
            enText = translate(raw_load["text"][count]["choices"][0]["jpText"])
            raw_load["text"][count]["choices"][0]["enText"] = enText

            print("Choice: ",raw_load["text"][count]["choices"][1]["jpText"])
            enText = translate(raw_load["text"][count]["choices"][1]["jpText"])
            raw_load["text"][count]["choices"][1]["enText"] = enText
        except KeyError:
            print("No choice")
        except IndexError:
            print("Only one choice")

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(raw_load, file, indent=4, ensure_ascii=False) 



def translate(rawText):
    api_key = config["server"]["api_key"]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    post_request = {
        "model" : config["server"]["model"],
        "temperature" : config["server"]["temperature"],
        "messages" : [
            {
                "role": "user", "content": rawText
            },
            {
                "role" : "system", "content" : f"{config['server']['system_prompt']} Refer to below for a dictionary in json format with the order japanese_text : english_text. (example\"ミホノブルボン\": \"Mihono Bourbon\", which means translate ミホノブルボン to Mihono Bourbon. \n {dictionary_json_str} \n translate the below text",
            }
        ],
        "max_completion_tokens" : "300",
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
        headers = headers,
        json = post_request
    )
    json_traslated = response.json()
    trans_text = json_traslated["choices"][0]["message"]["content"]
    print(f"Translation: {trans_text}")
    return trans_text

def transLoop():
    if not os.path.exists(target_folder):
        print("Folder does not exist")
        return
    print(f"Running through all files in {target_folder}")

    for root, _, files in os.walk(target_folder):
            for file_name in files:
                if file_name.endswith('.json'):
                    file_path = os.path.join(root, file_name)
                    process_json(file_path)    

transLoop()