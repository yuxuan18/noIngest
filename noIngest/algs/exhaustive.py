from noIngest.data_utils.data import Data
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
    pd.DataFrame(results).to_csv("temp.csv")
    count_result = data.get_count(results)
    avg_result = data.get_avg(results)
    print(count_result)
    print(avg_result)



if __name__ == "__main__":
    data = Data("../../data", partition=(41, 42))
    run_exhaustive_oracle(data)
    data.prep_features()
    run_exhaustive_reid(data, 0.9)