import pandas as pd
import click
import matplotlib.pyplot as plt
import altair as alt
import altair_ally as aly
import os

@click.command()
@click.option('--data_train_path', type=str, required=True, help='Path to the training data CSV file.')
@click.option('--output_dir', type=str, required=True, help='Directory to save the visualizations.')
def visualize_data(data_train_path, output_dir):
    """
    Creates visualizations and saves figures as PNG files.
    """
    # Load data
    data_train = pd.read_csv(data_train_path)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Enable VegaFusion for Altair
    aly.alt.data_transformers.enable('vegafusion')

    # Distribution plot for numerical features
    aly.dist(data_train, color='age_group').save(f"{output_dir}/fig_numeric_feats.png")
    aly.dist(data_train, color='age_group', dtype='object').save(f"{output_dir}/fig_categorical_feats.png")

    print(f"Saved distribution plots to {output_dir}")

    # Correlation heatmap
    numerical_features = data_train.select_dtypes(include=['float64']).columns
    correlation_matrix = data_train[numerical_features].corr()

    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(correlation_matrix, cmap="Reds", aspect="auto")

    ax.set_xticks(range(len(numerical_features)))
    ax.set_yticks(range(len(numerical_features)))
    ax.set_xticklabels(numerical_features, rotation=45, ha="right")
    ax.set_yticklabels(numerical_features)
    plt.colorbar(im, ax=ax)
    plt.title("Feature-Feature Correlation Heatmap", fontsize=14)
    plt.tight_layout()

    # Save the heatmap
    heatmap_path = f"{output_dir}/fig_feats_heatmap.png"
    plt.savefig(heatmap_path)
    print(f"Saved heatmap to {heatmap_path}")

if __name__ == "__main__":
    visualize_data()
