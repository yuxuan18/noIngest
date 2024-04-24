# screen -d -m python run_noingest.py --data_dir data/human --partition 1,2 --threshold 0.9
# screen -d -m python run_noingest.py --data_dir data/human --partition 2,3 --threshold 0.9
# screen -d -m python run_noingest.py --data_dir data/human --partition 3,4 --threshold 0.9
# screen -d -m python run_noingest.py --data_dir data/human --partition 4,5 --threshold 0.9
# screen -d -m python run_noingest.py --data_dir data/human --partition 5,6 --threshold 0.9
# screen -d -m python run_noingest.py --data_dir data/human --partition 6,7 --threshold 0.9

# screen -d -m python run_noingest.py --data_dir data/human --partition 1,2,3 --threshold 0.9
screen -d -m python run_noingest.py --data_dir data/human --partition 1,2,3,4 --threshold 0.9
screen -d -m python run_noingest.py --data_dir data/human --partition 1,2,3,4,5 --threshold 0.9
screen -d -m python run_noingest.py --data_dir data/human --partition 1,2,3,4,5,6 --threshold 0.9
screen -d -m python run_noingest.py --data_dir data/human --partition 1,2,3,4,5,6,7 --threshold 0.9