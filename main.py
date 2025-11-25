import json
import requests
import toml

raw_json = "raw/example.json"
translate_string = "驚くほど前向きで、頑張り屋で、地力が高い"

def process_json():
    print("Loading Json")
    count = -1
    with open(raw_json, "r", encoding="utf-8") as file:
        raw_load = json.load(file)
        run = True
        while run == True:
            count = count + 1
            try:
                print("Name: ",raw_load["text"][count]["jpName"])
                translate(raw_load["text"][count]["jpName"])
                print("Text: ",raw_load["text"][count]["jpText"])
                translate(raw_load["text"][count]["jpText"])
            except IndexError: 
                print("Finished!")
                break
            try:
                print("Choice: ",raw_load["text"][count]["choices"][0]["jpText"])
                translate(raw_load["text"][count]["choices"][0]["jpText"])
                print("Choice: ",raw_load["text"][count]["choices"][1]["jpText"])
                translate(raw_load["text"][count]["choices"][1]["jpText"])
            except KeyError:
                print("No choice")
            except IndexError:
                print("Only one choice")



def translate(rawText):
    with open("config.toml", "r") as f:
     config = toml.load(f)
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
                "role" : "system", "content" : config["server"]["system_prompt"]
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
    print(json_traslated["choices"][0]["message"]["content"])

process_json()