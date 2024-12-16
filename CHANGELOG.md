# Change Log
This file documents all notable changes made for this project. It is 
based on [Keep a Changelog](http://keepachangelog.com/).
 
## [Unreleased] - yyyy-mm-dd (TBD, estimating 2024-12-16)
 
These are changes we are still working on that are yet to be published.

***Highlight for this release***: Added unit tests for functions, this change log and various fixes from reviews by the instructors and our peers
 
### Added
- We abstracted some functions out of the scripts into utility functions in the [src](src) folder and 
added tests for them. The tests are in [test](test) folder, written 
using the [pytest](https://pytest.org/) framework
- A description of the variables in the data file have been added to the report
 
### Changed
 
### Fixed
- In the previous version, we were refitting the Logistic Regression 
model after using `GridSearchCV` to get the optimal hyperparameter values. This has now 
been corrected in "06_model_fitting.py". We save `best_estimator_` from the `GridSearchCV` 
object and use it in the subsequent steps.

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