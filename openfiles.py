import os
import json
from remove_posts import de_duplicate,delete_tweets

path = r"../apify/digital_ids" #path that includes the .json files (only) 

#Loop through all files in folder and clean them
for file in os.scandir(path):
    if file.is_file():
        data=[] # initialization of the data in the .json file 

        with open(file.path, "r") as f:
            print("Cleaning ", file.name, ":")
            data = json.load(f) # Load .json file for clean up
        
        #De-duplicate json data (remove duplicate tweets by id)
        unique_data = de_duplicate(data)

        #Delete noise (non-greek or non-greeklish tweets)
        denoised_data=delete_tweets(unique_data)

        # Overwrite file with cleaned data
        with open(file.path, "w", encoding="utf-8") as f:
            json.dump(denoised_data, f, indent=4)

