import os
from os import walk
import json
import pandas as pd
import epiweeks
from epiweeks import Week
from datetime import date as convert_to_date
import numpy as np
import argparse
import config
import shutil
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def create_dataset(root, source):
    """
    This function creates DATASET/ and annotations/ folder.  
    
    Parameters:

        root(string) - path to dataset folder
    """
    dest = os.path.join(root, "images")
    shutil.copytree(source, dest)    
    os.makedirs(os.path.join(root, "annotations"), exist_ok=True)

def get_epiweek(image_name, numeric = False):
    """
    Obtain the epidemiological week (epiweek) given an image name containing the date when the image was taken.

    Parameters:
    - image_name (str): Image name containing the collection week.
    - numeric (bool): If True, return the epiweek as an integer. If False (default), return it as a string.

    Returns:
    - epiweek (int or str): Corresponding epiweek for the given month and year.
    """
    if numeric: 
        date = image_name.split('_')[1].split('.')[0]
        year, month, day = map(int, image_name.split('_')[1].split('.')[0].split('-'))
        date = convert_to_date(year, month, day)
        epiweek = str(Week.fromdate(date))
        epiweek = int(epiweek)
        
    else: 
        date = image_name.split('-')
        # Get year as int
        year = ''.join(filter(str.isdigit, date[0]))
        year = int(year)
        # Get month as int
        month = ''.join(filter(str.isdigit, date[1]))
        month = int(month)
        # Get day as int
        day = ''.join(filter(str.isdigit, date[2]))
        day = int(day)
        # Get epiweek:
        date = convert_to_date(year, month, day)
        epiweek = str(Week.fromdate(date))
        epiweek = int(epiweek)
    return epiweek


def get_label(path):
    # Get city:
    city = path.split('/')[1]
    # Get epiweek:
    date = path.split('/')[2]
    epiweek = get_epiweek(date)
    # Get cases:
    cases = int(df[df['Municipality'] == city].loc[:,epiweek])
    return cases 


def run():
    root = "/Users/sebasmos/Desktop/DATASETS/DATASET_81_cities_v1.0/DATASET_final_satellite_extractor"
    climatic_data_path = config.climatic_data_path
    socioeco_data_path = config.socioeco_data_path
    binary_classification = config.binary_classification
    incidence_ratio = config.incidence_ratio
    multiclass_labels = config.multiclass_labels
    # Read files
    data = pd.read_csv(climatic_data_path)
    socioeco_data = pd.read_csv(socioeco_data_path)
    binary_classification = pd.read_csv(binary_classification)
    incidence_ratio = pd.read_csv(incidence_ratio)
    multiclass_labels = pd.read_csv(multiclass_labels)
    # We select indexes 468-624 to filter based on Satellite images availabilty: image_2016-01-01 - 2018-12-23
    # 459-624 to inclide since 2015-11-1
    data = data[468:624].reset_index(drop=True)

    # Create data folder
    f = os.listdir(root)

    print(f"Collected data for processing: ", f)
    for idx in range(0,len(f)): # getting 1 image for 1 epiweek
        folder = os.path.join(root, f[idx])
        if not f[idx].isdigit():
            print(f"Skipping non-numeric folder: {f[idx]}")
            continue

        code_per_image = int(f[idx])
        print(f"Processing municipality {code_per_image}")
        folder_name = f[idx]
        images = sorted(os.listdir(folder))
        counter = 0
        counter_bv = 0
        for img in images:     
            counter_bv +=1
            image_path  = os.path.join("DATASET", "images", folder_name, img)
            # import pdb;pdb.set_trace()
            date_img = get_epiweek(img, numeric = True) # image date
            date_csv = [get_epiweek(date, numeric = False) for date in data.date]
            data["indexer"] = date_csv
            # print(f"{counter}/{len(images)}")
            if date_img in date_csv:
                # Number of cases and environmental data
                row = data[data["indexer"]==date_img]
                # Binary classification labels
                col_bin_cases = binary_classification[["Municipality code", str(date_img)]]
                # Incidence_ratio
                col_incidence_ratio_cases = incidence_ratio[["Municipality code", str(date_img)]]
                # Multilabel
                col_multiclass_cases = multiclass_labels[["Municipality code", str(date_img)]]  
                # 
                full_codes= row.columns
                
                for e in full_codes:
                    name = e.split("_")[0]
                    if len(e.split("_"))>1:
                        code = int(e.split("_")[1])
                        if code == code_per_image: 
                            ####  Obtain socio-Economical data - Downsampling because data is per-year-sampled :/
                            socioeco_row = socioeco_data[socioeco_data["Municipality code"]==code]
                            year = int(str(date_img)[:4]) # Only obtain year to downsample with it
                            name = "Population"+str(year)
                            #### Binary cases
                            cases_bin = int(col_bin_cases[col_bin_cases["Municipality code"]==int(code)][str(date_img)])
                            #### Incidence ratio
                            cases_incidence = int(col_incidence_ratio_cases[col_incidence_ratio_cases["Municipality code"]==int(code)][str(date_img)])
                            #### Multi-label
                            cases_multiclass_labels = int(col_multiclass_cases[col_multiclass_cases["Municipality code"]==int(code)][str(date_img)])
                
                            ## Create JSON file
                            anns_folder = os.path.join(root, "annotations", folder_name)
                            os.makedirs(anns_folder, exist_ok=True)
                            
                            anns_path = os.path.join(root, anns_folder, image_path.split("/")[-1:][0][:-5] + ".json")

                            out_file = open(anns_path, "w")  
                            if len(str(code))<5:
                                code = "0"+ str(code)
                            counter+=1
                            #assert counter_bv ==counter, "Different fectchers"
                            annotation = {
                                        "image_path": image_path,
                                        "municipality_code": int(code),
                                        "epiweeks": date_img,
                                        "dynamic":{
                                                    "cases" :{
                                                                "dengue_cases": (np.array(row["cases" + "_" + str(int(code))])).tolist()[0], # how to get the index, given that we have the column and the the date
                                                                "binary_classification":cases_bin,
                                                                #"incidence_rate": cases_incidence,
                                                                "multiclass": cases_multiclass_labels,
                                                    },
                                                    "environmental_data": { "temperature": (np.array(row["temperature" + "_" + str(code)]).tolist()),
                                                                            "precipitation": (np.array(row["precipitation" + "_" + str(code)])).tolist(),
                                                                          },
                                                    "socioeconomic_data":{
                                                                            "Population": [int(socioeco_row[name]) if name in socioeco_row.columns else 0][0],
                                                    }
                                        },
                                        "static":
                                                    {
                                                    "environmental_data": {
                                                                            "elevation": float(socioeco_row["Elevation"])
                                                                          },

                                                    "socioeconomic_data": {
                                                                            "Age0-4(%)": float(socioeco_row["Age0-4(%)"]),
                                                                            'Age5-14(%)':float(socioeco_row["Age15-29(%)"]),
                                                                            'Age>30(%)':float(socioeco_row["Age>30(%)"]),
                                                                            'AfrocolombianPopulation(%)':float(socioeco_row["AfrocolombianPopulation(%)"]),  
                                                                            'IndianPopulation(%)':float(socioeco_row["IndianPopulation(%)"]), 
                                                                            'PeoplewithDisabilities(%)':float(socioeco_row["PeoplewithDisabilities(%)"]),    
                                                                            'Peoplewhocannotreadorwrite(%)':float(socioeco_row["Peoplewhocannotreadorwrite(%)"]), 
                                                                            'Secondary/HigherEducation(%)':float(socioeco_row["Secondary/HigherEducation(%)"]),  
                                                                            'Employedpopulation(%)':float(socioeco_row["Employedpopulation(%)"]),  
                                                                            'Unemployedpopulation(%)':float(socioeco_row["Unemployedpopulation(%)"]),  
                                                                            'Unemployedpopulation(%)':float(socioeco_row["Unemployedpopulation(%)"]),  
                                                                            'Peopledoinghousework(%)':float(socioeco_row["Peopledoinghousework(%)"]),  
                                                                            'Men(%)':float(socioeco_row["Men(%)"]),  
                                                                            'Women(%)':float(socioeco_row["Women(%)"]),
                                                                            'Householdswithoutwateraccess(%)':float(socioeco_row["Householdswithoutwateraccess(%)"]), 
                                                                            'Householdswithoutinternetaccess(%)':float(socioeco_row["Householdswithoutinternetaccess(%)"]), 
                                                                            'Buildingstratification1(%)':float(socioeco_row["Buildingstratification1(%)"]), 
                                                                            'Buildingstratification2(%)':float(socioeco_row["Buildingstratification2(%)"]), 
                                                                            'Buildingstratification3(%)':float(socioeco_row["Buildingstratification3(%)"]), 
                                                                            'Buildingstratification4(%)':float(socioeco_row["Buildingstratification4(%)"]), 
                                                                            'Buildingstratification5(%)':float(socioeco_row["Buildingstratification5(%)"]), 
                                                                            'Buildingstratification6(%)':float(socioeco_row["Buildingstratification6(%)"]), 
                                                                            'NumberofhospitalsperKm2':float(socioeco_row["NumberofhospitalsperKm2"]),  
                                                                            'NumberofhousesperKm2':float(socioeco_row["NumberofhousesperKm2"]),  
                                                                           }
                                                    }
                                        }
                            
                        

                            json.dump(annotation, out_file, indent=6) 
                            out_file.close()
    print("Done.")


if __name__ == "__main__":

    run()