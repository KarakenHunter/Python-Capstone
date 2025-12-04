# Author: Manthan Sharma
# Roll No. 2501410037

import os
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

DATA_DIR = Path("data")
OUT_DIR = Path("output")
OUT_DIR.mkdir(exist_ok=True)

TS_CANDIDATES = ["timestamp", "time", "datetime", "date", "ts"]
KWH_CANDIDATES = ["kwh", "energy", "consumption", "usage", "meter"]
BUILDING_COL_CANDIDATES = ["building", "site", "facility"]


def find_csv_files(data_dir=DATA_DIR):
    if not data_dir.exists():
        print(f"data folder not found at {data_dir}. Create it and add sample csvs.")
        return []
    return list(data_dir.glob("*.csv"))

def try_read_csv(fp):
    # try reading and handle mildly corrupt files
    try:
        df = pd.read_csv(fp, on_bad_lines="skip")
        return df
    except FileNotFoundError:
        print(f"File not found: {fp}")
        return None
    except Exception as e:
        print(f"Failed to read {fp}: {e}")
        return None

def detect_and_rename_cols(df, filename):
    df.columns = df.columns.str.strip()
    col_map = {c: c.lower().strip() for c in df.columns}

    # find timestamp col
    ts_col = None
    for c in df.columns:
        if c.lower().strip() in TS_CANDIDATES:
            ts_col = c
            break
    # find kwh col
    kwh_col = None
    for c in df.columns:
        if c.lower().strip() in KWH_CANDIDATES:
            kwh_col = c
            break
    # find building col
    b_col = None
    for c in df.columns:
        if c.lower().strip() in BUILDING_COL_CANDIDATES:
            b_col = c
            break

    rename_d = {}
    if ts_col:
        rename_d[ts_col] = "timestamp"
    if kwh_col:
        rename_d[kwh_col] = "kwh"
    if b_col:
        rename_d[b_col] = "building"

    df = df.rename(columns=rename_d)

    if "timestamp" not in df.columns:
        first_col = df.columns[0]
        df = df.rename(columns={first_col: "timestamp"})

    if "kwh" not in df.columns:
        # try second column
        if len(df.columns) > 1:
            second_col = df.columns[1]
            df = df.rename(columns={second_col: "kwh"})
        else:
            # no kwh data, create dummy zeros so pipeline continues
            df["kwh"] = 0

    if "building" not in df.columns:
        bname = Path(filename).stem.split("_")[0]
        df["building"] = bname

    return df

def ingest_all():
    files = find_csv_files()
    if not files:
        print("No CSV files found in data/. Put some sample files and rerun.")
        return pd.DataFrame()
    all_dfs = []
    bad_files = []
    for fp in files:
        df = try_read_csv(fp)
        if df is None:
            bad_files.append(str(fp))
            continue
        df = detect_and_rename_cols(df, fp)
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        # ensure kwh is numeric
        df["kwh"] = pd.to_numeric(df["kwh"], errors="coerce")
        before = len(df)
        df = df.dropna(subset=["timestamp", "kwh"])
        after = len(df)
        if after == 0:
            print(f"Warning: {fp} has no valid rows after parsing, skipping.")
            bad_files.append(str(fp))
            continue
        all_dfs.append(df)
        print(f"Loaded {fp} ({before}->{after} rows kept)")
    if bad_files:
        print("Some files failed to load:", bad_files)
    if not all_dfs:
        return pd.DataFrame()
    df_all = pd.concat(all_dfs, ignore_index=True)
    # normalize column order and names
    df_all = df_all[["building", "timestamp", "kwh"]]
    # sort by time
    df_all = df_all.sort_values("timestamp").reset_index(drop=True)
    return df_all

# Task 2: Aggregation logic
def calculate_daily_totals(df):
    df = df.set_index("timestamp")
    daily = df.groupby("building").resample("D")["kwh"].sum().reset_index()
    return daily

def calculate_weekly_aggregates(df):
    df = df.set_index("timestamp")
    weekly = df.groupby("building").resample("W")["kwh"].sum().reset_index()
    return weekly

def building_wise_summary(df):
    s = (df.groupby("building")["kwh"]
         .agg(total="sum", mean="mean", mn="min", mx="max")
         .reset_index())
    s["mean"] = s["mean"].round(2)
    return s

# Task 3: OOP modeling
class MeterReading:
    def __init__(self, ts, kwh):
        self.ts = pd.to_datetime(ts)
        self.kwh = float(kwh)

class Building:
    def __init__(self, name):
        self.name = name
        self.reads = [] 

    def add_reading(self, r: MeterReading):
        self.reads.append(r)

    def total(self):
        return sum(r.kwh for r in self.reads)

    def daily_series(self):
        if not self.reads:
            return pd.DataFrame()
        df = pd.DataFrame([{"timestamp": r.ts, "kwh": r.kwh} for r in self.reads])
        df = df.set_index("timestamp").resample("D")["kwh"].sum().reset_index()
        return df

    def peak_hour(self):
        if not self.reads:
            return None
        max_r = max(self.reads, key=lambda x: x.kwh)
        return max_r.ts, max_r.kwh

class BuildingManager:
    def __init__(self):
        self.blds = {} 

    def ingest_from_df(self, df):
        # df has building,timestamp,kwh
        for _, row in df.iterrows():
            b = row["building"]
            if b not in self.blds:
                self.blds[b] = Building(b)
            try:
                r = MeterReading(row["timestamp"], row["kwh"])
                self.blds[b].add_reading(r)
            except Exception as e:
                continue

    def summary_df(self):
        rows = []
        for name, b in self.blds.items():
            rows.append({
                "building": name,
                "total_kwh": b.total(),
                "peak_ts": (b.peak_hour()[0] if b.peak_hour() else pd.NaT),
                "peak_kwh": (b.peak_hour()[1] if b.peak_hour() else np.nan)
            })
        return pd.DataFrame(rows)


# Task 4: Visualing the data
def make_dashboard(df_all, daily_df, weekly_df, out_path=OUT_DIR / "dashboard.png"):
    # daily line for all buildings
    plt.style.use('ggplot')
    fig, axs = plt.subplots(3, 1, figsize=(12, 14), constrained_layout=True)

    ax = axs[0]
    for name, grp in daily_df.groupby("building"):
        ax.plot(grp["timestamp"], grp["kwh"], label=name)
    ax.set_title("Daily Consumption Trend (kWh)")
    ax.set_xlabel("Date")
    ax.set_ylabel("kWh")
    ax.legend(fontsize="small", loc="best")

    ax = axs[1]
    # compute avg weekly per building
    avg_week = weekly_df.groupby("building")["kwh"].mean().sort_values(ascending=False)
    avg_week.plot(kind="bar", ax=ax)
    ax.set_title("Average Weekly Consumption per Building")
    ax.set_xlabel("Building")
    ax.set_ylabel("Avg kWh per week")

    ax = axs[2]

    peaks = df_all.groupby("building")["kwh"].max().reset_index()
    xs = np.arange(len(peaks))
    ax.scatter(xs, peaks["kwh"])
    ax.set_xticks(xs)
    ax.set_xticklabels(peaks["building"], rotation=45, ha="right")
    ax.set_title("Peak Single-Measurement Consumption by Building")
    ax.set_ylabel("kWh")

    fig.suptitle("Campus Energy Dashboard", fontsize=16)
    fig.savefig(out_path)
    plt.close(fig)
    print(f"Saved dashboard to {out_path}")

# Task 5: Output files
def save_outputs(df_clean, summary_df_build, out_dir=OUT_DIR):
    cleaned_fp = out_dir / "cleaned_energy_data.csv"
    summary_fp = out_dir / "building_summary.csv"
    txt_fp = out_dir / "summary.txt"

    # cleaned data
    df_clean.to_csv(cleaned_fp, index=False)
    # building summary
    summary_df_build.to_csv(summary_fp, index=False)

    # write summary
    total = df_clean["kwh"].sum()
    top_row = summary_df_build.sort_values("total_kwh", ascending=False).iloc[0]

    top_bld = top_row["building"]
    top_total = top_row["total_kwh"]
    # peak load time
    idx = df_clean["kwh"].idxmax()
    peak_ts = df_clean.loc[idx, "timestamp"]
    peak_val = df_clean.loc[idx, "kwh"]

    with open(txt_fp, "w") as f:
        f.write("Campus Energy Summary\n")
        f.write("=====================\n\n")
        f.write(f"Total campus consumption (kWh): {total:.2f}\n")
        f.write(f"Highest-consuming building: {top_bld} ({top_total:.2f} kWh)\n")
        f.write(f"Peak single reading: {peak_val:.2f} kWh at {peak_ts}\n\n")
        f.write("Notes:\n")
        f.write("- Data aggregated from multiple building CSV files\n")
        f.write("- Summary includes daily and weekly aggregations\n")
    print(f"Saved cleaned CSV -> {cleaned_fp}")
    print(f"Saved building summary -> {summary_fp}")
    print(f"Saved text summary -> {txt_fp}")

# Main function
def main():
    print("Starting ingestion...")
    df = ingest_all()
    if df.empty:
        print("No data ingested. Exiting.")
        return

    print("Computing aggregates...")
    daily = calculate_daily_totals(df)
    weekly = calculate_weekly_aggregates(df)
    bsummary = building_wise_summary(df)

    # create OOP objects 
    manager = BuildingManager()
    manager.ingest_from_df(df)
    manager_summary = manager.summary_df()
    mgr_ren = manager_summary.rename(columns={"total_kwh": "total_kwh", "peak_kwh": "peak_kwh"})
    # align column names for save
    bsummary_for_save = mgr_ren.copy()
    if "peak_kwh" not in bsummary_for_save.columns:
        bsummary_for_save["peak_kwh"] = np.nan
    # visual output
    make_dashboard(df, daily, weekly)
    # prepare df_clean for persistence (ensure timestamp serialized as ISO)
    df_clean = df.copy()
    df_clean["timestamp"] = pd.to_datetime(df_clean["timestamp"])
    save_outputs(df_clean, bsummary_for_save)

    print("All done.")

main()