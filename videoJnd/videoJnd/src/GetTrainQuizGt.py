import json

training_gt = './videoJnd/data/training_videos.json'
quiz_gt = './videoJnd/data/quiz_videos.json'

def get_training_gt() -> tuple:
    with open(training_gt,'r') as f:
        traing_gt_json = json.load(f)
        return traing_gt_json

def get_quiz_gt() -> tuple:
    with open(quiz_gt,'r') as f:
        quiz_gt_json = json.load(f)
        return quiz_gt_json
    

if __name__ == "__main__":
    pass