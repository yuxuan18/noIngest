from noIngest.data_utils.data import Data
from noIngest.estimate import Estimate
import pandas as pd

def run_exhaustive_oracle(data: Data):
    all_detect_ids = []
    for table_detects in data.detects.values():
        all_detect_ids.append(table_detects["detect_id"].to_list())
    results = data.get_predicate(all_detect_ids)
    count_result = data.get_count(results)
    avg_result = data.get_avg(results)
    print(count_result)
    print(avg_result)

def run_exhaustive_reid(data: Data, threshold: float):
    results = data.get_feature_predicate(-1, threshold)
    count_result = data.get_count(results)
    avg_result = data.get_avg(results)
    cost = sum(data.get_num_detects().values()) + sum(data.get_num_frames().values())
    estimate = Estimate(avg_result, -1, -1, count_result, -1, -1, 1, cost)
    partition_str = [str(part) for part in data.partition]
    partition_str = "_".join(partition_str)
    estimate.save(f"exhaustive_{partition_str}.jsonl")

if __name__ == "__main__":
    data = Data("../../data/vehicle", partition=(41, 42))
    # run_exhaustive_oracle(data)
    data.prep_features()
    run_exhaustive_reid(data, 0.9)