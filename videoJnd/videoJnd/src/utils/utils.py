def _convert_result(result:list) -> list:
    """
    just for adding result to the response for using postman better
    """

    for res in result:
        res["decision"] = "no decision"
        res["start_time"] = 1615709137
        res["end_time"] = 1615709387

    return result


if __name__ == "__main__":
    result = [
            {
                "vuid": "c4541aaf-5913-4994-a5db-059f25a0f787",
                "side": "L",
                "qp": "38",
                "url": "https://datasets.vqa.mmsp-kn.de/JND_datasets/Video_JND_dataset/JND_264_640x480/SRC105_640x480_24/crf_05/videoSRC105_640x480_24_qp_00_38_L_crf_05.mp4"
            },
            {
                "vuid": "25fa396c-8dac-4689-a76d-89ce2f1101a9",
                "side": "R",
                "qp": "21",
                "url": "https://datasets.vqa.mmsp-kn.de/JND_datasets/Video_JND_dataset/JND_264_640x480/SRC001_640x480_30/crf_05/videoSRC001_640x480_30_qp_00_21_R_crf_05.mp4"
            }
        ]

    result = _convert_result(result)

    result = str(result).replace("\'", "\"")
    # result = eval(result)


    print(result)
