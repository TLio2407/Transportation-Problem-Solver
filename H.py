import kagglehub

# Download latest version
path = kagglehub.dataset_download("uciml/internet-advertisements-data-set")

print("Path to dataset files:", path)