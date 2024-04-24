from noIngest.algs.stratified_oracle import run_stratified_oracle
from noIngest.data_utils.data import Data
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, required=True)
    parser.add_argument("--partition", type=str, required=True)
    parser.add_argument("--threshold", type=float, required=True)

    args = parser.parse_args()

    data = Data(args.data_dir, partition=tuple(map(int, args.partition.split(","))))
    for prob in [0, 0.1, 0.2, 0.3, 0.4]:
        for rate in [0.1, 0.15, 0.2, 0.25, 0.3]:
            run_stratified_oracle(data, rate, prob)
