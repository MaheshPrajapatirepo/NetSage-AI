import subprocess

print("Step 1 - Collecting logs")
subprocess.run(
    ["python", "Main_Folder/src/log_collector.py"]
)

print("Step 2 - Parsing logs")
subprocess.run(
    ["python", "Main_Folder/src/log_parser.py"]
)

print("Step 3 - Feature Engineering")
subprocess.run(
    ["python", "Main_Folder/src/feature_engineering.py"]
)

print("Pipeline Complete")

print("Step 4 - Inference")
subprocess.run(
    ["python", "Main_Folder/src/inference.py"]
)