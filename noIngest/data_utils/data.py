import pandas as pd
import pickle
import numpy as np
from typing import List, Union, Literal

class Data:
    def __init__(self, data_path: str="data", partition: tuple=(41, 42)) -> None:
        self.partition = partition
        self.path = data_path
        self._read_files()

    def _read_files(self):
        # read detects
        self.detects = {}
        for part in self.partition:
            self.detects[part] = pd.read_csv(f"{self.path}/detects/{part}.csv")
        
        # read groundtruth
        partition_str = [str(part) for part in self.partition]
        groundtruth_filename = "groundtruth_" + "_".join(partition_str) + ".csv"
        n_part = len(partition_str)
        self.groundtruth = pd.read_csv(f"{self.path}/groundtruth/{n_part}/{groundtruth_filename}")

    def prep_features(self):
        # read features
        self.features = {}
        for part in self.partition:
            self.features[part] = np.load(f"{self.path}/features/{part}.npy")
    
    def get_num_detects(self):
        return {part: len(self.detects[part]) for part in self.detects}

    def get_gt_avg(self):
        # self join
        matched_detects = self.groundtruth.merge(self.groundtruth, on="object_id").query("camera_id_x != camera_id_y")[["detect_id_x", "detect_id_y"]]
        # join first two detect to get frame ids
        part1, part2 = self.partition[:2]
        result = matched_detects.merge(self.detects[part1], left_on="detect_id_x", right_on="detect_id")[["detect_id_y", "frame_id"]]
        result = result.merge(self.detects[part2], left_on="detect_id_y", right_on="detect_id")[["frame_id_x", "frame_id_y"]]
        return np.abs(result["frame_id_x"] - result["frame_id_y"]).mean()

    def get_gt_count(self):
        return len(
            self.groundtruth.merge(self.groundtruth, on="object_id").query("camera_id_x != camera_id_y")["detect_id_x"].unique()
        )

    def get_count(self, matched_tuples: np.ndarray):
        return np.unique(matched_tuples.T[0]).shape[0]

    def get_avg(self, matched_tuples: np.ndarray):
        columns = [f"detect_id_T{i}" for i in range(len(matched_tuples[0]))]
        matched_tuples_df = pd.DataFrame(matched_tuples, columns=columns)
        part1, part2 = self.partition[:2]
        table1 = self.detects[part1]
        table2 = self.detects[part2]
        matched_tuples_df = matched_tuples_df.merge(table1, how="inner", left_on="detect_id_T0", right_on="detect_id")
        matched_tuples_df = matched_tuples_df.merge(table2, how="inner", left_on="detect_id_T1", right_on="detect_id")
        return np.abs(matched_tuples_df["frame_id_x"] - matched_tuples_df["frame_id_y"]).mean()
    
    def get_predicate(self, detect_id_package: List[List[int]]) -> np.ndarray:
        assert len(self.partition) == len(detect_id_package)
        labeled_detect_id_packages = []
        for camera_id, detect_ids in zip(self.partition, detect_id_package):
            camera_groundtruth = self.groundtruth[self.groundtruth.camera_id == camera_id]
            detect_ids_df = pd.DataFrame(detect_ids, columns=["detect_id"])
            labeled_camera_result = detect_ids_df.merge(camera_groundtruth, how="inner", on="detect_id")[["detect_id", "object_id"]]
            labeled_detect_id_packages.append(labeled_camera_result)

        curr_results = pd.DataFrame()
        for i in range(len(labeled_detect_id_packages)):
            table = labeled_detect_id_packages[0]
            assert isinstance(table, pd.DataFrame)
            if i == 0:
                curr_results = table.rename(columns={"detect_id": "T0_id"})
                continue
            curr_results = curr_results.merge(table, how="inner", on="object_id")
            new_col = f"T{i}_id"
            curr_results = curr_results.rename(columns={"detect_id": new_col})
        return curr_results.to_numpy()

    def get_prob_predicate(self, detect_id_package: List[List[int]], prob: float) -> np.ndarray:
        positive_tuples_array = self.get_predicate(detect_id_package)
        n_drop = int(len(positive_tuples_array) * prob)
        id_keep = np.random.choice(len(positive_tuples_array), size=len(positive_tuples_array)-n_drop, replace=False)
        return positive_tuples_array[id_keep]
        
    def _get_all_feature_predicate(self, threshold) -> pd.DataFrame:
        all_features = [self.features[part] for part in self.partition]
        curr_results = self._sim_join(threshold, all_features)
        return curr_results

    def _sim_join(self, threshold, all_features):
        pairwise_results = []
        for i in range(len(all_features) - 1):
            feature_l = all_features[i]
            feature_r = all_features[i+1]
            scores = feature_l @ feature_r.T
            print(np.max(scores), np.min(scores))
            scores += 1
            scores /= 2
            positive_pairs = np.array(np.where(scores >= threshold)).T
            positive_pairs = pd.DataFrame(positive_pairs, columns=["l", "r"])
            pairwise_results.append(positive_pairs)
        
        curr_results = pd.DataFrame()
        for i in range(len(pairwise_results)):
            table = pairwise_results[i]
            assert isinstance(table, pd.DataFrame)
            if i == 0:
                curr_results = table.rename(columns={
                    "l": "T0",
                    "r": "T1"
                })
                continue
            left_on = f"T{i}"
            curr_results = curr_results.merge(table, how="inner", left_on=left_on, right_on="l")
            curr_results = curr_results.drop(columns=["l"])
            new_col = f"T{i+1}"
            curr_results = curr_results.rename(columns={"r": new_col})
        return curr_results

    def get_feature_predicate(self, 
                              detect_id_package: Union[List[List[int]], Literal[-1]], 
                              threshold: float) -> np.ndarray:
        if detect_id_package == -1:
            return self._get_all_feature_predicate(threshold).to_numpy()
        else:
            assert len(detect_id_package) == len(self.partition)
            all_feats = []
            for table_detect_id, part in zip(detect_id_package, self.partition):
                feat = self.features[part][table_detect_id]
                all_feats.append(feat)
            results = self._sim_join(threshold, all_feats)
            original_columns = [col for col in results.columns]
            for col in original_columns:
                table_detect_id = detect_id_package[int(col[1:])]
                results[col+"_id"] = results[col].map(lambda x: table_detect_id[x])
            results = results.drop(columns=original_columns)
            return results.to_numpy()