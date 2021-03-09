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
codec = config["CODEC"]

url_str = "JND_{codec}_640x480/SRC{src_name}_640x480_{frame_rate}/crf_{crf}/videoSRC{src_name}_640x480_{frame_rate}_qp_00_qpV_{side}_crf_{crf}.mp4"

def side() -> str:
    return ["L", "R"][random.randint(0,1)]

def gen_url_str(prefix:str, codec:str, src_name:str, frame_rate:str, crf:str, side:str) -> str:
    postfix = url_str.format(codec=codec, src_name=src_name, frame_rate=frame_rate, crf=crf, side=side)
    url = prefix + postfix
    return url

def gen_src_urls() -> list:
    src_urls = []
    f_24_videos = frame_rate["24"]
    f_30_videos = frame_rate["30"]

    for _src_name in src_name:
        for _crf in crf:
            for _codec in codec:
                if _src_name in f_24_videos:
                    _frame_rate = 24
                elif _src_name in f_30_videos:
                    _frame_rate = 30

                    src_urls.append(gen_url_str(url_prefix, _codec, _src_name, _frame_rate, _crf, side()))

    return src_urls

# TODO: check all urls
if __name__ == "__main__":
    print(gen_src_urls())
