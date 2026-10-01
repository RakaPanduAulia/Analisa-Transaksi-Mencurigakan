from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker

fake = Faker("id_ID")
rng = np.random.default_rng(42)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

CUSTOMER_COUNT = 100
TRANSACTION_COUNT = 1_000

def generate_customers(count: int) -> pd.DataFrame:
    """Membuat transaksi sintis dengan beberapa anomali yang sengaja dimasukkan."""
    start = pd.Timestamp("2025-01-01")
    end = pd.Timestamp("2025-01-31 23:59:59")
    seconds_in_range = int((end - start).total_seconds())

    timestamps = [
        start + pd.Timedelta(seconds=int(x))
        for x in rng.integers(0,  seconds_in_range, size=TRANSACTION_COUNT)
    ]

    df = pd.DataFrame({
        "transcation_id": [f"TRX{i:05d}" for i in range(TRANSACTION_COUNT + 1)],
        "customer_id": [
            f"CUST{x:04d}"
            for x in rng.integers(1, CUSTOMER_COUNT + 1, size=TRANSACTION_COUNT)
        ],
        "timestamp": timestamps,
        "amount": np.round(rng.lognormal(mean=11, sigma=0.8, size=TRANSACTION_COUNT), 2),
        "merchant": [fake.company() for _ in range(TRANSACTION_COUNT)],
        "city": [fake.city() for _ in range(TRANSACTION_COUNT)],
    })

    # Tandai anomali
    df["injected_anomaly"] = False