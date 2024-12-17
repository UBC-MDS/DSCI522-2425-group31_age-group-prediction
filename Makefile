.PHONY: all clean

all: reports/age_prediction_report.html reports/age_prediction_report.pdf

# Download and extract data
data/raw/NHANES_age_prediction.csv/: scripts/01_download_data.py
	python scripts/01_download_data.py \
		--url="https://archive.ics.uci.edu/static/public/887/national+health+and+nutrition+health+survey+2013-2014+(nhanes)+age+prediction+subset.zip" \
		--output_dir=data/raw

# Clean, validate, and save processed data
data/processed/cleaned.csv: scripts/02_clean_validate_save_data.py data/raw/NHANES_age_prediction.csv/
	python scripts/02_clean_validate_save_data.py \
		--input_path=data/raw/NHANES_age_prediction.csv \
		--output_path=data/processed/cleaned.csv

# Split data into training and testing datasets
data/processed/data_train.csv data/processed/data_test.csv: scripts/03_split_preprocess_data.py data/processed/cleaned.csv
	python scripts/03_split_preprocess_data.py \
		--input_path=data/processed/cleaned.csv \
		--output_dir=data/processed \
		--seed=123

# Visualize data
results/figures/fig_numeric_feats.png results/figures/fig_feats_heatmap.png: scripts/05_visualize_and_save.py data/processed/data_train.csv
	python scripts/05_visualize_and_save.py \
		--data_train_path=data/processed/data_train.csv \
		--output_dir=results/figures

# Train and tune the model
results/models/age_prediction_preprocessor.pickle results/models/age_prediction_model.pickle results/figures/fig_hyperparameter_c.png: scripts/06_model_fitting.py data/processed/data_train.csv
	python scripts/06_model_fitting.py \
		--train-data=data/processed/data_train.csv \
		--preprocessor-to=results/models \
		--pipeline-to=results/models \
		--plot-to=results/figures \
		--seed=123

# Evaluate the model
results/tables/age_model_report.csv results/tables/confusion_matrix.csv: scripts/07_model_evaluation.py results/models/age_prediction_model.pickle data/processed/data_test.csv
	python scripts/07_model_evaluation.py \
		--model-path=results/models/age_prediction_model.pickle \
		--test-data=data/processed/data_test.csv \
		--results-to=results/tables

# Build HTML and PDF reports
reports/age_prediction_report.html reports/age_prediction_report.pdf: reports/age_prediction_report.qmd \
    results/models/age_prediction_model.pickle \
    results/figures/fig_numeric_feats.png \
    results/figures/fig_feats_heatmap.png \
    results/figures/fig_hyperparameter_c.png \
    results/tables/age_model_report.csv \
    results/tables/confusion_matrix.csv
	quarto render reports/age_prediction_report.qmd --to html
	quarto render reports/age_prediction_report.qmd --to pdf

# Clean up intermediate and output files
clean:
	rm -rf data/raw/*
	rm -rf data/processed/*
	rm -rf results/models/*
	rm -rf results/figures/*
	rm -rf results/tables/*
	rm -rf reports/age_prediction_report.html \
	       reports/age_prediction_report.pdf \
	       reports/age_prediction_report_files