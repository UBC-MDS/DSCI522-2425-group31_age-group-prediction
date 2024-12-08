import requests
import zipfile
import os
import click

@click.command()
@click.option('--url', type=str, required=True, help='URL of the dataset to download.')
@click.option('--output_dir', type=str, required=True, help='Directory to save the extracted data.')
def download_data(url, output_dir):
    """
    Downloads and extracts the dataset from the given URL.
    """
    zip_path = os.path.join(output_dir, "data.zip")
    os.makedirs(output_dir, exist_ok=True)

    response = requests.get(url)
    with open(zip_path, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded dataset to {zip_path}")

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
    print(f"Extracted data to {output_dir}")

if __name__ == "__main__":
    download_data()
