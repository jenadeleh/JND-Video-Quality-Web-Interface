import json

cfg_path = './videoJnd/config.json'
# cfg_path = '../config.json'

def get_config() -> tuple:
    with open(cfg_path,'r') as f:
        config = json.load(f)
    return config

if __name__ == "__main__":
    pass