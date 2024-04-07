from noIngest.data_utils.data import Data
import numpy as np
import pandas as pd

def run_fixed_rate(data: Data, threshold: float, rate: float):
    all_detect_ids = []
    for table_detects in data.detects.values():
        total_num_frames = len(table_detects["frame_id"].unique())
        num_selected_frames = int(total_num_frames * rate)
        selected_frames = np.linspace(0, total_num_frames-1, num_selected_frames)
        selected_frames = [int(x) for x in selected_frames]
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
    data = Data("../../data", partition=(41, 42, 43))
    data.prep_features()
    run_fixed_rate(data, 0.9, 0.1)
    