import os
import json

path = r"../apify/digital_ids" #path that includes the .json files (only) 

#Loop through all files in folder and clean them
for file in os.scandir(path):
    if file.is_file():
        data=[] # initialization of the data in the .json file 

        with open(file.path, "r") as f:
            print("Cleaning ", file.name, ":")
            data = json.load(f) # Load .json file for clean up
        
        