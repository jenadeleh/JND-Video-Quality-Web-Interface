def _convert_result(result:list) -> list:
    """
    just for adding result to the response for using postman better
    """

    for res in result:
        res["decision"] = "R"
        res["start_time"] = 1615709137
        res["end_time"] = 1615709387

    return result


if __name__ == "__main__":
    result = [
            {
                "vuid": "9e407fcf-29f8-4980-bf87-68bf9caee015",
                "side": "L",
                "qp": "24",
                "url": "https://datasets.vqa.mmsp-kn.de/JND_datasets/Video_JND_dataset/JND_264_640x480/SRC001_640x480_30/crf_12/videoSRC001_640x480_30_qp_00_24_L_crf_12.mp4"
            },
            {
                "vuid": "2c320fa6-2692-43a7-9976-18aac444b4d6",
                "side": "L",
                "qp": "30",
                "url": "https://datasets.vqa.mmsp-kn.de/JND_datasets/Video_JND_dataset/JND_264_640x480/SRC105_640x480_24/crf_12/videoSRC105_640x480_24_qp_00_30_L_crf_12.mp4"
            }
        ]

    result = _convert_result(result)

    result = str(result).replace("\'", "\"")
    # result = eval(result)


    print(result)
