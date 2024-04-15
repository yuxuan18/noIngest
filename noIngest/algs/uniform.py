from noIngest.data_utils.data import Data
from noIngest.estimate import Estimate
import numpy as np
import pandas as pd


def run_uniform(data: Data, threshold: float, rate: float):
    all_detect_ids = []
    cost = 0
    for table_detects in data.detects.values():
        total_num_frames = len(table_detects["frame_id"].unique())
        num_selected_frames = int(total_num_frames * rate)
        selected_frames = np.random.choice(total_num_frames, size=num_selected_frames, replace=False)
        cost += len(selected_frames)
        selected_frames_df = pd.DataFrame(selected_frames, columns=["frame_id"])
        selected_detect_ids = selected_frames_df.merge(table_detects, how="inner", on="frame_id")["detect_id"]
        cost += len(selected_detect_ids)
        all_detect_ids.append(selected_detect_ids)
    restuls = data.get_feature_predicate(all_detect_ids, threshold=threshold)
    count_est, count_lb, count_ub = data.get_count_w_ci(restuls)
    avg_est, avg_lb, avg_ub = data.get_avg_w_ci(restuls)
    estimate = Estimate(avg_est, avg_lb, avg_ub, count_est, count_lb, count_ub, rate, cost)
    partition_str = [str(part) for part in data.partition]
    partition_str = "_".join(partition_str)
    estimate.save(f"results/stratified_{partition_str}.jsonl")

if __name__ == "__main__":
    data = Data("../../data/vehicle", partition=(41, 42))
    data.prep_features()
    run_uniform(data, 0.9, 0.1)