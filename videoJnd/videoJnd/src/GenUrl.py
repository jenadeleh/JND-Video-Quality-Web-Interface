import random
from videoJnd.src.GetConfig import get_config

# from GetConfig import get_config

config = get_config()
URL_PREFIX = config["URL_PREFIX"]
url_postfix = config["URL_POSTFIX"]



def gen_video_url(codec:str
                , src_name:str
                , frame_rate:str
                , crf:str
                , qp:str
                , side) -> str:
    """
    input: the parameters of the video
    output: the URL of this video, and its side
    """

    postfix = url_postfix.format(codec = codec
                            , src_name = src_name
                            , frame_rate = frame_rate
                            , qp = qp
                            , crf = crf
                            , side = side)

    url = URL_PREFIX + postfix
    return url

def random_side() -> str:
    return ["L", "R"][random.randint(0,1)]


# src_name = config["SRC_NAME"]
# video_per_group = config["VIDEO_PER_GROUP"]
# rating_times_per_src = config["RATING_PER_SRC"]

# frame_rate = config["FRAME_RATE"]
# crf = config["CRF"]
# codec = config["CODEC"]

# def gen_all_video_urls() -> list:
#     src_urls = []
#     f_24_videos = frame_rate["24"]
#     f_30_videos = frame_rate["30"]

#     for _src_name in src_name:
#         for _crf in crf:
#             for _codec in codec:
#                 if _src_name in f_24_videos:
#                     _frame_rate = 24
#                 elif _src_name in f_30_videos:
#                     _frame_rate = 30

#                     src_urls.append(gen_url_str(url_prefix, _codec, _src_name, _frame_rate, _crf, side()))

#     return src_urls

# TODO: check all urls

if __name__ == "__main__":
    # print(gen_all_video_urls())
    pass
