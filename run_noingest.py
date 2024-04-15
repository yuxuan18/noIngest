from noIngest.algs.exhaustive import run_exhaustive_reid
from noIngest.algs.stratified import run_stratified
from noIngest.algs.fixed_rate import run_fixed_rate
from noIngest.algs.uniform import run_uniform
from noIngest.data_utils.data import Data
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, required=True)
    parser.add_argument("--partition", type=str, required=True)
    parser.add_argument("--threshold", type=float, required=True)

    args = parser.parse_args()

    data = Data(args.data_dir, partition=tuple(map(int, args.partition.split(","))))
    run_exhaustive_reid(data, args.threshold)
    for rate in [0.1, 0.15, 0.2, 0.25, 0.3]:
        run_fixed_rate(data, args.threshold, rate)
        for _ in range(100):
            run_stratified(data, args.threshold, rate)
            run_uniform(data, args.threshold, rate)