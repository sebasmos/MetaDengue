# DengueSet

DengueSet is a unified dataset format that combines satellite imagery and Socioeconomical and environmental metadata.

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

## Download DengueSet *Augmented data with aligned metadata* [Download](https://console.cloud.google.com/storage/browser/colombia_sebasmos/DATASET_augmented/DATASET_augmented_v1/annotations/23001?pageState=(%22StorageObjectListTable%22:(%22f%22:%22%255B%255D%22))&project=mit-hst-dengue&prefix=&forceOnObjectsSortingFiltering=false):
Google CLoud Platform bucket storing 10 top cities. . Data extracted using recursive artifact removal, cloud removal based on LeastCC, and Nearest Interpolation for spatial resolution. Implemented [here] and augmentations applied to RGB channels while leaving other satellite channels unchanged:
 
1. Contrast limited adaptive histogram equalization (CLAHE) - using  clip_limit=6.0 and  tile_grid_size=(16, 16)
1. RGBShift (applied to 30 pixels per channel with 100 % probability )
1. RandomBrightnessContrast (applied with a probability of 50% probability)

[
## Create metadata dataset.

In order to create a customized dataset, please update `config.py` with the corresponding metadata and adapt `build_dataset.py` as required. For DengueSet case, please run `build_dataset.py`. Afterwards, make sure the `images` folder is stored on the same tree hierarchy as the `annotations/` folder.


## Metadata organization: 

```
{ 
      {
      "image_path": "DATASET/images/50001/image_2016-01-03.tiff",
      "municipality_code": 50001,
      "date": 201601,
      "labels": {
            "cases": 27,
            "binary_classification": 0,
            "incidence_ratio": 0,
            "multilabel": 0
      },
      "metadata": {
            "environmental_data": {
                  "temperature": [
                        29.906313774134105
                  ],
                  "precipitation": [
                        0.0346768693251678
                  ],
                  "elevation": 323.0
            },
            "socioeconomic_data": {
                  "Population": 512787,
                  "Age0-4(%)": 6.82,
                  "Age5-14(%)": 26.75,
                  "Age>30(%)": 50.63,
                  "AfrocolombianPopulation(%)": 0.93,
                  "IndianPopulation(%)": 0.36,
                  "PeoplewithDisabilities(%)": 4.33,
                  "Peoplewhocannotreadorwrite(%)": 3.22,
                  "Secondary/HigherEducation(%)": 62.3,
                  "Employedpopulation(%)": 40.08,
                  "Unemployedpopulation(%)": 5.75,
                  "Peopledoinghousework(%)": 12.71,
                  "Men(%)": 49.33,
                  "Women(%)": 50.67,
                  "Householdswithoutwateraccess(%)": 5.99,
                  "Householdswithoutinternetaccess(%)": 36.51,
                  "Buildingstratification1(%)": 21.672,
                  "Buildingstratification2(%)": 21.0672,
                  "Buildingstratification3(%)": 27.9166,
                  "Buildingstratification4(%)": 3.6941,
                  "Buildingstratification5(%)": 1.5769,
                  "Buildingstratification6(%)": 0.4983,
                  "NumberofhospitalsperKm2": 0.173648,
                  "NumberofhousesperKm2": 111.006093
            }
      }
}
```

