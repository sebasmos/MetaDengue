# MetaDengue

MetaDengue is a unified dataset format that combines satellite imagery and Socioeconomical and environmental metadata.

DengueSet seeks to organize satellite imagery and metadata using a unified and standard dataset, that can be scalable and reproduceable to any geographical area. For this particular project, we have extracted the satellite imagery of the municialities of Colombia from 2016 to 2018 based on the Epiweek using [satellite extractor](https://github.com/sebasmos/satellite.extractor), a proposal based on SentinelHub, and with this proposal we combine Socioeconomical and environmental metadata in JSON files, one for each corresponding image so that the data is temporally and spacially aligned. 


## Proposed Structure 

The following is the desired structured that we propose for DengueSet. There are 2 main folders, one called `images` which contains a subfolder for each corresponding municipality and inside of it, all the temporal satellite imagery for each corresponding municipality. On the second folder, the same structure as the previous one, but on each case, containing the corresponding metadata on JSON files.

```
DATASET/ 
	images/
		5001/
                  images_01_01_2016.tiff
                  images_01_07_2016.tiff
                  .
                  .
		5002/
    .
    .
		500N/
	annotations/
		5001/
                  images_01_01_2016.json
                  images_01_07_2016.json
		      .
                  .
		5002
    .
    .
		500N
```


## Create metadata dataset.

In order to create a customized dataset, please update `config.py` with the corresponding metadata and adapt `build_dataset.py` as required. For DengueSet case, please run `build_dataset.py`. Afterwards, make sure the `images` folder is stored on the same tree hierarchy as the `annotations/` folder.


## Metadata organization: 

```
{
      "image_path": "DATASET/images/23001/image_2016-01-03.tiff",
      "municipality_code": 23001,
      "epiweek": 201601,
      "dynamic": {
            "cases": {
                  "dengue_cases": 31,
                  "binary_classification": 1,
                  "multiclass_classification": 0
            },
            "environmental_data":{
                  "temperature": [
                        30.703164269355987
                  ],
                  "precipitation": [
                        0.1678038044754522
                  ]
            }
      },
      "static": {
            "environmental_data": {
                  "elevation": 36.0
            },
            "socio_economic_demographic_data": {
                  "socio_economic_data":{
                        "Secondary/HigherEducation(%)": 59.93,
                        "Employedpopulation(%)": 36.46,
                        "Unemployedpopulation(%)": 4.61,
                        "Peopledoinghousework(%)": 17.02,
                        "Householdswithoutwateraccess(%)": 10.07,
                        "Householdswithoutinternetaccess(%)": 52.84,
                        "Buildingstratification1(%)": 60.2975,
                        "Buildingstratification2(%)": 14.4266,
                        "Buildingstratification3(%)": 6.6937,
                        "Buildingstratification4(%)": 2.3756,
                        "Buildingstratification5(%)": 0.8777,
                        "Buildingstratification6(%)": 0.7190000000000001,
                        "NumberofhospitalsperKm2": 0.087552,
                        "NumberofhousesperKm2": 37.051894
                  },
                  "socio_demographic_data":{
                        "Age0-4(%)": 7.76,
                        "Age5-14(%)": 26.31,
                        "Age>30(%)": 48.69,
                        "Men(%)": 48.51,
                        "Women(%)": 51.49,
                        "Population per year": 471724,
                        "AfrocolombianPopulation(%)": 1.7,
                        "IndianPopulation(%)": 0.71,
                        "Peoplewhocannotreadorwrite(%)": 5.93,
                        "PeoplewithDisabilities(%)": 2.69
                  }
            }
      }
}
```

## Download DengueSet *Augmented data with aligned metadata* [[Download](https://console.cloud.google.com/storage/browser/colombia_sebasmos/DATASET_augmented/DATASET_augmented_v1/annotations/23001?pageState=(%22StorageObjectListTable%22:(%22f%22:%22%255B%255D%22))&project=mit-hst-dengue&prefix=&forceOnObjectsSortingFiltering=false)]:
Google CLoud Platform bucket storing 10 top cities. . Data extracted using recursive artifact removal, cloud removal based on LeastCC, and Nearest Interpolation for spatial resolution. Implemented [here] and augmentations applied to RGB channels while leaving other satellite channels unchanged:
 
1. Contrast limited adaptive histogram equalization (CLAHE) - using  clip_limit=6.0 and  tile_grid_size=(16, 16)
1. RGBShift (applied to 30 pixels per channel with 100 % probability )
1. RandomBrightnessContrast (applied with a probability of 50% probability)

## Dataloder demos

Define custom dataloders in `dataloders/`

Pytorch implementation [[Notebeook](https://github.com/sebasmos/MetaDengue/blob/main/PytorchDataloders%20demo.ipynb)]

1. Custom dataloader to load all folders within `DATASET/images` folder. [[Here](https://github.com/sebasmos/MetaDengue/blob/main/dataloaders/vanilla_dataloader.py)] 
1. Custom dataloder to load *filtered* folders within `DATASET/image` folder. [[Here](https://github.com/sebasmos/MetaDengue/blob/main/dataloaders/filtered_dataloader.py)]
      

Tensorflow implementation [[Notebook](https://github.com/sebasmos/MetaDengue/blob/main/TensorFlowDataloders%20demo.ipynb)] 
1. Custom dataloader to load all folders within `DATASET/images` folder. [[Here](https://github.com/sebasmos/MetaDengue/blob/main/dataloaders/tfvanilla_dataloader.py)]
1. Custom dataloder to load *filtered* folders within `DATASET/image` folder. [[Here](https://github.com/sebasmos/MetaDengue/blob/main/dataloaders/tffiltered_dataloader.py)]
