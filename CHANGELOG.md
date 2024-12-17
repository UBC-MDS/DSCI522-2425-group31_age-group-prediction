# Change Log
This file documents all notable changes made for this project. It is 
based on [Keep a Changelog](http://keepachangelog.com/).
 
## [3.0.0] - 2024-12-16
 
Added unit tests for functions, this change log and various fixes from reviews by the instructors and our peers
which are highlighted and linked in the ***Fixed*** section below.
 
### Added
- We abstracted some functions out of the scripts into utility functions in the [src](src) folder and 
added tests for them. The tests are in [test](test) folder, written 
using the [pytest](https://pytest.org/) framework

- A description of the variables in the data file have been added to the report (#c50401ae9c8b039205f5750774df3a05c89500ba)
to resolve [the third comment in this peer review](https://github.com/UBC-MDS/data-analysis-review-2024/issues/28#issuecomment-2530156986)

- Link to the report in the README file in commit [41f788d](https://github.com/UBC-MDS/DSCI522-2425-group31_age-group-prediction/commit/41f788d869626636a97c4ed224a54b73bd00bf4d)
as suggested by two [reviwers](https://github.com/UBC-MDS/data-analysis-review-2024/issues/28#issuecomment-2530156986)
 
### Changed



### Fixed

- Based on the second [peer review comment by Green-zy](https://github.com/UBC-MDS/data-analysis-review-2024/issues/28#issuecomment-2530385608), we updated the report "Method and Analysis section" to indicate that we will use F1 
Score as a metric due to the class imbalance in this [commit](https://github.com/UBC-MDS/DSCI522-2425-group31_age-group-prediction/commit/905a54bdb44464c385c5743a7256556c06f0d94a).

- In the previous version, we were refitting the Logistic Regression 
model after using `GridSearchCV` to get the optimal hyperparameter values. This has now 
been corrected in "06_model_fitting.py". We save `best_estimator_` from the `GridSearchCV` 
object and use it in the subsequent steps. This was fixed by commit [05f6d74](https://github.com/UBC-MDS/DSCI522-2425-group31_age-group-prediction/commit/05f6d7436adf9dae9da6e906b863d3913c1e8464)
with thanks to review by [Shannon](https://github.com/UBC-MDS/data-analysis-review-2024/issues/28#issuecomment-2530156986)

- Altair dependency changed from 'altair-all=5.4.*' to 'altair-all=5.4.1' as per instructor feedback from Week 2
and also highlighted by peer review from [Shawn](https://github.com/UBC-MDS/data-analysis-review-2024/issues/28#issuecomment-2530404242)

### Closed

- We appreciate the first comment from [review by Green-zy](https://github.com/UBC-MDS/data-analysis-review-2024/issues/28#issuecomment-2530385608). However the suggestion is not aligned with the objective of our study.
We therefore closed the issue with no further action

-The fourth comment in the [same review](https://github.com/UBC-MDS/data-analysis-review-2024/issues/28#issuecomment-2530385608), suggested adding DOI metadata in the references. We searched and validated
the URLs provided and added 2 of those related that were used in for reference in our project. In addition, we found
and updated 2 other [references](https://github.com/UBC-MDS/DSCI522-2425-group31_age-group-prediction/commit/c50401ae9c8b039205f5750774df3a05c89500ba).


## [2.0.0] - 2024-12-08
  
- Abstracted code from `*.ipynb` notebook to [scripts](scripts) folder
- Created the literate [report](reports/age_prediction_report.qmd)
 
### Added
 
### Changed
  
- Literate [report](reports/age_prediction_report.qmd) extracted from ipynb and created as Quarto Markdown file
 
### Fixed
 
- Instructions in the README file on how to run the analysis

## [1.0.0] - 2024-11-30
  
- Created the analysis in a docker image, published on DockerHub
 
### Added

- Automatically build docker image and publish to [Docker Hub](https://hub.docker.com/) when Dockerfile is modified
 
### Changed

- README to reflect running analysis in a docker image
 
### Fixed
 
- Pinned exact versions for dependencies in the [environment.yaml](environment.yaml)
 
## [0.0.1] - 2024-11-23

- Initial release with the entire analysis in an .ipynb file
 
### Added

- This was the initial release. All files were created during this release
- Entire analysis code and report contained in [notebook/age_prediction_report.ipynb](notebook/age_prediction_report.ipynb)
- Created dependencies in environment.yaml and conda-lock.yml
- Created the License and Code of Conduct for the project