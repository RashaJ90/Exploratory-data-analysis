import pandas as pd
import requests
import io

URL = "REPLACE-THIS-WITH-THE-URL-OF-THE-CSV-FILE"  # REPLACE-THIS-WITH-THE-URL-OF-THE-CSV-FILE


def create_dataset(path: str = URL):
    download = requests.get(path).content
    return pd.read_csv(io.StringIO(download.decode('utf-8')))
