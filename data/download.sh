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

# if the dataset is human
if [ "$dataset" == "human" ]; then
  # download the vehicle dataset
  gdown 16Dw7B-VubtS5M9H4vDGpc7G5Iexu4RFv
  echo "decompressing the dataset..."
  unzip features_human.zip
  ls
  mv features_human human/features
  echo "done, cleaning up..."
  rm features_human.zip
fi