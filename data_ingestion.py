import io
import os
import time
from pathlib import Path

import pandas as pd
import requests

from election_simulation import main as run_simulation

DATA_DIR = Path(__file__).resolve().parent / "data"
POLLING_DATA_PATH = DATA_DIR / "polling_data.csv"


def fetch_polling_data(source_url: str | None = None) -> pd.DataFrame:
    """Fetch raw polling data from an HTTP endpoint or local file.

    Parameters
    ----------
    source_url:
        URL of the polling dataset. If ``None``, the function will attempt
        to read from ``POLLING_API_URL`` environment variable. If that is
        also undefined, the existing local ``polling_data.csv`` file is used.
    """

    url = source_url or os.environ.get("POLLING_API_URL")
    if url:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        if url.endswith(".csv"):
            return pd.read_csv(io.StringIO(response.text))
        return pd.DataFrame(response.json())
    return pd.read_csv(POLLING_DATA_PATH)


def clean_polling_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the polling dataframe to match simulation requirements."""
    required_cols = [
        "state_name",
        "harris_support",
        "trump_support",
        "weight",
        "moe",
    ]
    df = df[required_cols]
    df = df.dropna(subset=required_cols)
    df["harris_support"] = pd.to_numeric(df["harris_support"], errors="coerce")
    df["trump_support"] = pd.to_numeric(df["trump_support"], errors="coerce")
    df["weight"] = pd.to_numeric(df["weight"], errors="coerce").fillna(1).astype(int)
    df["moe"] = pd.to_numeric(df["moe"], errors="coerce")
    df = df.dropna(subset=required_cols)
    return df


def save_polling_data(df: pd.DataFrame, path: Path = POLLING_DATA_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def ingest_once(update_simulation: bool = True) -> None:
    """Fetch, clean and save polling data then optionally rerun simulation."""
    df = fetch_polling_data()
    df = clean_polling_data(df)
    save_polling_data(df)
    print(f"Saved {len(df)} rows to {POLLING_DATA_PATH}")
    if update_simulation:
        run_simulation()


def schedule_ingestion(interval_hours: float = 24) -> None:
    """Continuously ingest polling data at a fixed interval."""
    while True:
        try:
            ingest_once(update_simulation=True)
        except Exception as exc:  # pragma: no cover
            print(f"Polling data ingestion failed: {exc}")
        time.sleep(interval_hours * 3600)


if __name__ == "__main__":
    interval = float(os.environ.get("POLLING_UPDATE_INTERVAL_HOURS", 24))
    if os.environ.get("RUN_ONCE"):
        ingest_once(update_simulation=True)
    else:
        schedule_ingestion(interval_hours=interval)
