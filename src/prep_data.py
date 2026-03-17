"""ETL script: download CSV and convert to Parquet.

Run once before launching app.py:
    python prep_data.py

This script demonstrates the typical ETL prep step:
  raw CSV (large, row-oriented) → Parquet (columnar, compressed, fast)

"""

from pathlib import Path

import duckdb

# NYC TLC also publishes the same data as CSV (larger, uncompressed)
CSV_URL = "https://raw.githubusercontent.com/UBC-MDS/DSCI-532_2026_34_BikeShareOptimizer/refs/heads/main/data/raw/201306-citibike-tripdata.csv"
OUT = Path(__file__).parent / ".." / "data" / "processed" / "201306-citibike-tripdata.parquet"

OUT.parent.mkdir(exist_ok=True)

print(f"Reading CSV from {CSV_URL} ...")
print("Converting to Parquet (this takes a minute — runs only once) ...")

# read_csv_auto infers headers and column types automatically
duckdb.execute(f"""
    COPY (SELECT * FROM read_csv_auto('{CSV_URL}'))
    TO '{OUT}' (FORMAT PARQUET)
""")

size_mb = OUT.stat().st_size / 1e6
print(f"Saved → {OUT}  ({size_mb:.1f} MB)")
print("Parquet is 5-10x faster for filtered queries — DuckDB only reads needed columns.")
print("\nReady. Run: shiny run src/app.py")
