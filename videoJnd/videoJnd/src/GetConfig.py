import json

cfg_path = './videoJnd/config.json'
# cfg_path = '../config.json'

def get_config() -> tuple:
    with open(cfg_path,'r') as f:
        data = json.load(f)
    return (data["CALC_UPPER_NUM"], data["GROUP_NUM"], data["SRC_VIDEO_NUM"])

if __name__ == "__main__":
    pass