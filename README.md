# Age Group Predictor

  - author: Dongchun Chen, Ismail Bhinderwala, Rashid Mammadov & Sienko Ikhabi

A data analysis project for DSCI 522 (Data Science workflows); a
course in the Master of Data Science program at the University of
British Columbia.

## Project Summary

Here we attempt to build a classification model using the Logistic Regression
algorithm which can predict whether an individual belongs to the senior (≥65 years) age group or 
the non-senior (<65 years) age group based on specific features. The model utilizes a supervised machine 
learning algorithm to identify patterns and relationships within the dataset to make accurate predictions.

The dataset used in this project is a subset of the National Health and Nutrition Examination Survey (NHANES) 2013-2014, 
created by the Centers for Disease Control and Prevention (CDC). The subset was donated on September 21, 2023, 
and is designed for predicting respondents' age. The dataset can be found 
[here](https://archive.ics.uci.edu/dataset/887/national+health+and+nutrition+health+survey+2013-2014+(nhanes)+age+prediction+subset).
The NHANES dataset collects extensive health and nutritional information from a diverse U.S. population, and this 
particular subset narrows the focus to selected features hypothesized to correlate strongly with age.

## Usage

First time running the project,
run the following from the root of this repository:

``` bash
conda-lock install --name 522-group31 conda-lock.yml
```

To run the analysis,
run the following from the root of this repository:

``` bash
jupyter lab 
```

Open `age_prediction_report.ipynb` in Jupyter Lab
and under Switch/Select Kernel choose 
"Python [conda env:522-group31]".

Next, under the "Kernel" menu click "Restart Kernel and Run All Cells...".

## Dependencies

- `conda` (version 23.9.0 or higher)
- `conda-lock` (version 2.5.7 or higher)
- `jupyterlab` (version 4.0.0 or higher)
- `nb_conda_kernels` (version 2.3.1 or higher)
- Python and packages listed in [`environment.yml`](environment.yml)

## License

The analysis report contained herein are licensed under the
[Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) License](https://creativecommons.org/licenses/by-nc-sa/4.0/).
See [the license file](LICENSE.md) for more information. If
re-using/re-mixing please provide attribution and link to this webpage.
The software code contained within this repository is licensed under the
MIT license. See [the license file](LICENSE.md) for more information.



