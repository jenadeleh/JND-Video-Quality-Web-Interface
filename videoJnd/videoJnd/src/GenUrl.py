import random
from videoJnd.src.GetConfig import get_config

# from GetConfig import get_config

config = get_config()

src_name = config["SRC_NAME"]
video_per_group = config["VIDEO_PER_GROUP"]
rating_times_per_src = config["RATING_TIMES_PER_SRC"]
url_prefix = config["URL_PREFIX"]
frame_rate = config["FRAME_RATE"]
crf = config["CRF"]

url_str = "SRC{src_name}_640x480_{frame_rate}/crf_{crf}/videoSRC{src_name}_640x480_{frame_rate}_qp_00_qpV_{side}_crf_{crf}.mp4"

def side() -> str:
    return ["L", "R"][random.randint(0,1)]

def gen_url_str(prefix:str, src_name:str, frame_rate:str, crf:str, side:str) -> str:
    postfix = url_str.format(src_name=src_name, frame_rate=frame_rate, crf=crf, side=side)
    url = prefix + postfix
    return url

def gen_src_urls() -> list:
    urls = []
    for prefix in url_prefix:
        for src in src_name:
            for fr in frame_rate:
                for c in crf:
                    urls.append(gen_url_str(prefix, src, fr, c, side()))

    return urls

# TODO: check all urls
if __name__ == "__main__":
    print(gen_src_urls())
