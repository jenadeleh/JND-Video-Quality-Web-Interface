import random
from videoJnd.src.GetConfig import get_config

def gen_url(src, crf):
    config = get_config()
    url_prefix = config["URL_PREFIX"]
    side = ["L", "R"][random.randint(0,1)]
    pass

if __name__ == "__main__":
    pass