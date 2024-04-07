dataset=$1
if [ -z "$dataset" ]; then
  echo "Usage: $0 <dataset>"
  exit 1
fi

# if the dataset is vehicle
if [ "$dataset" == "vehicle" ]; then
  # download the vehicle dataset
  gdown 1oKMHGwZbLXmi6CLwTzAQbBzU3-MEqwrK
  echo "decompressing the dataset..."
  tar -xf features.tar
  mv features vehicle
  echo "done, cleaning up..."
  rm features.tar
fi