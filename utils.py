import requests
import pandas as pd
from io import BytesIO, StringIO

def get_dataframe_from_github_release(url, encoding='utf-8', is_binary=False, **read_csv_kwargs):
    """
    Downloads a CSV from a GitHub release and loads it into a pandas DataFrame.
    
    Parameters:
    - url (str): Direct download URL of the dataset from the GitHub release.
    - encoding (str): Encoding format of the CSV. Default is 'utf-8'.
    - is_binary (bool): Set True if the CSV is compressed (e.g., bz2, zip).
    - **read_csv_kwargs: Additional arguments for pd.read_csv()

    Returns:
    - pd.DataFrame if successful, or error message (str)
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raises HTTPError for bad status codes

        if is_binary:
            buffer = BytesIO(response.content)
        else:
            buffer = StringIO(response.content.decode(encoding))
        df = pd.read_csv(buffer, **read_csv_kwargs)
        return df
    except requests.exceptions.RequestException as e:
        return f"Download failed: {e}"
    except Exception as e:
        return f"Error processing CSV: {e}"