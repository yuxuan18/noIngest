from noIngest.data_utils.data import Data
import numpy as np
import pandas as pd


def run_uniform(data: Data, threshold: float, rate: float):
    all_detect_ids = []
    for table_detects in data.detects.values():
        total_num_frames = len(table_detects["frame_id"].unique())
        num_selected_frames = int(total_num_frames * rate)
        selected_frames = np.random.choice(total_num_frames, size=num_selected_frames, replace=False)
        selected_frames_df = pd.DataFrame(selected_frames, columns=["frame_id"])
        selected_detect_ids = selected_frames_df.merge(table_detects, how="inner", on="frame_id")["detect_id"]
        print(len(selected_detect_ids)/len(table_detects))
        all_detect_ids.append(selected_detect_ids)
    restuls = data.get_feature_predicate(all_detect_ids, threshold=threshold)
    count_result = data.get_count(restuls)
    avg_result = data.get_avg(restuls)
    print(count_result/rate)
    print(avg_result)

if __name__ == "__main__":
    data = Data("../../data", partition=(41, 42))
    data.prep_features()
    run_uniform(data, 0.9, 0.2)