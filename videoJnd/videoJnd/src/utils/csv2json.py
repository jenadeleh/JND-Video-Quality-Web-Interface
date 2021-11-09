import json
import pandas as pd
df = pd.read_csv("training_videos.csv")
df['crf'] = df['crf'].astype("string")
df['qp'] = df['qp'].astype("string")

columns = ['ref_video', 'presentation', 'crf', 'qp', 'videos_pair','side_of_reference', 'ground_truth']
data = {}
data['video_pairs'] = []

for index, row in df.iterrows():
  row_dict = {}
  for c in columns:
    row_dict[c] = row[c].strip()
  data['video_pairs'].append(row_dict)


with open('training_videos.json', 'w') as outfile:
    json.dump(data, outfile)

