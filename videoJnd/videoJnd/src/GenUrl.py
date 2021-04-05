import random

def gen_video_url(URL_PREFIX:str
                , URL_POSTFIX:str
                , codec:str
                , src_name:str
                , frame_rate:str
                , crf:str
                , qp:str
                , side) -> str:
    """
    input: the parameters of the video
    output: the URL of this video, and its side
    """

    postfix = URL_POSTFIX.format(codec = codec
                            , src_name = src_name
                            , frame_rate = frame_rate
                            , qp = qp
                            , crf = crf
                            , side = side)

    url = URL_PREFIX + postfix
    return url

def random_side() -> str:
    return ["L", "R"][random.randint(0,1)]

if __name__ == "__main__":
    # print(gen_all_video_urls())
    pass
