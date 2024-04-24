from noIngest.data_utils.data import Data
from noIngest.estimate import Estimate
import numpy as np
import pandas as pd

def run_stratified_oracle(data: Data, rate: float, prob: float):
    all_detect_ids = []
    cost = 0

    for i, table_detects in enumerate(data.detects.values()):
        total_num_frames = len(table_detects["frame_id"].unique())

        # select anchor frames
        num_selected_frames = int(total_num_frames * 0.01)
        selected_frames = np.linspace(0, total_num_frames-1, num_selected_frames)
        selected_frames = [int(x) for x in selected_frames]
        if selected_frames[-1] != total_num_frames - 1:
            selected_frames.append(total_num_frames - 1)
        selected_frames_df = pd.DataFrame(selected_frames, columns=["frame_id"])
        selected_detect_ids = selected_frames_df.merge(table_detects, how="inner", on="frame_id")[["frame_id", "detect_id"]]
        
        anchor_frame_num_detects = []
        for frame_id in selected_frames:
            num_detects = selected_detect_ids[selected_detect_ids["frame_id"] == frame_id].shape[0]
            anchor_frame_num_detects.append([frame_id, num_detects])
        
        # calculate allocation ratio
        total_num_detects = 0
        for j in range(len(anchor_frame_num_detects)-1):
            total_num_detects += anchor_frame_num_detects[j][1] + anchor_frame_num_detects[j+1][1]
        total_num_sampled_frames = int(total_num_frames * rate)
        # sample frames
        sampled_frames = []
        for j in range(len(anchor_frame_num_detects)-1):
            start_frame = anchor_frame_num_detects[j][0]
            end_frame = anchor_frame_num_detects[j+1][0]
            ratio = (anchor_frame_num_detects[j][1] + anchor_frame_num_detects[j+1][1]) / total_num_detects
            num_sampled_frames = int(total_num_sampled_frames * ratio) + 1
            print(start_frame, end_frame, num_sampled_frames)
            sample = np.random.choice(range(start_frame, end_frame), num_sampled_frames, replace=True)
            sampled_frames += sample.tolist()
        cost += len(sampled_frames)
        # get detects
        sampled_frames_df = pd.DataFrame(sampled_frames, columns=["frame_id"])
        sampled_detect_ids = sampled_frames_df.merge(table_detects, how="inner", on="frame_id")["detect_id"]
        all_detect_ids.append(sampled_detect_ids)
        cost += len(sampled_detect_ids)

    restuls = data.get_prob_predicate(all_detect_ids, prob)
    count_est, count_lb, count_ub = data.get_count_w_ci(restuls)
    avg_est, avg_lb, avg_ub = data.get_avg_w_ci(restuls)
    partition_str = [str(part) for part in data.partition]
    partition_str = "_".join(partition_str)
    estimate = Estimate(avg_est, avg_lb, avg_ub, count_est, count_ub, count_lb, rate, cost, prob=prob)
    estimate.log()
    estimate.save(f"results/sensi_{partition_str}.jsonl")

if __name__ == "__main__":
    data = Data("../../data/vehicle", partition=(41, 42))
    run_stratified_oracle(data, 0.2, 0.1)
    