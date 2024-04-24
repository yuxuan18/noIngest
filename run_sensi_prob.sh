screen -d -m python run_noingest_sensi.py --data_dir data/human --partition 1,2 --threshold 0.9
screen -d -m python run_noingest_sensi.py --data_dir data/vehicle --partition 41,42 --threshold 0.9
