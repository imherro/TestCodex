"""Fetch Postal Savings Bank of China A-share data with AKShare.

Default target:
- Name: 邮储银行
- A-share code: 601658
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import akshare as ak
import pandas as pd


DEFAULT_SYMBOL = "601658"
DEFAULT_NAME = "邮储银行"
DATE_PATTERN = re.compile(r"^\d{8}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch all available A-share data for Postal Savings Bank of China."
    )
    parser.add_argument("--symbol", default=DEFAULT_SYMBOL, help="A-share code, default: 601658")
    parser.add_argument("--name", default=DEFAULT_NAME, help="Stock name, default: 邮储银行")
    parser.add_argument(
        "--start-date",
        default="19700101",
        help="Start date in YYYYMMDD format, default: 19700101",
    )
    parser.add_argument(
        "--end-date",
        default="20500101",
        help="End date in YYYYMMDD format, default: 20500101",
    )
    parser.add_argument(
        "--period",
        default="daily",
        choices=("daily", "weekly", "monthly"),
        help="K-line period, default: daily",
    )
    parser.add_argument(
        "--adjust",
        default="",
        choices=("", "qfq", "hfq"),
        help="Adjustment mode: empty for unadjusted, qfq for forward, hfq for backward",
    )
    parser.add_argument(
        "--output-dir",
        default="data",
        type=Path,
        help="Directory to write CSV files, default: data",
    )
    return parser.parse_args()


def validate_yyyymmdd(value: str, field_name: str) -> None:
    if not DATE_PATTERN.match(value):
        raise ValueError(f"{field_name} must be in YYYYMMDD format, got: {value}")


def write_csv(df: pd.DataFrame, path: Path) -> None:
    if df.empty:
        raise RuntimeError(f"No data returned for {path.name}")
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"saved {len(df):,} rows -> {path}")


def fetch_history(
    symbol: str,
    period: str,
    start_date: str,
    end_date: str,
    adjust: str,
) -> pd.DataFrame:
    return ak.stock_zh_a_hist(
        symbol=symbol,
        period=period,
        start_date=start_date,
        end_date=end_date,
        adjust=adjust,
    )


def fetch_stock_info(symbol: str) -> pd.DataFrame:
    return ak.stock_individual_info_em(symbol=symbol)


def fetch_spot_snapshot(symbol: str, name: str) -> pd.DataFrame:
    spot_df = ak.stock_zh_a_spot_em()
    if "代码" in spot_df.columns:
        matched = spot_df[spot_df["代码"].astype(str) == symbol]
        if not matched.empty:
            return matched
    if "名称" in spot_df.columns:
        matched = spot_df[spot_df["名称"].astype(str) == name]
        if not matched.empty:
            return matched
    raise RuntimeError(f"Could not find spot quote for {name}({symbol})")


def main() -> None:
    args = parse_args()
    validate_yyyymmdd(args.start_date, "--start-date")
    validate_yyyymmdd(args.end_date, "--end-date")

    args.output_dir.mkdir(parents=True, exist_ok=True)

    adjust_suffix = args.adjust or "none"
    hist_path = args.output_dir / f"psbc_{args.symbol}_hist_{args.period}_{adjust_suffix}.csv"
    info_path = args.output_dir / f"psbc_{args.symbol}_info.csv"
    spot_path = args.output_dir / f"psbc_{args.symbol}_spot.csv"

    history_df = fetch_history(
        symbol=args.symbol,
        period=args.period,
        start_date=args.start_date,
        end_date=args.end_date,
        adjust=args.adjust,
    )
    info_df = fetch_stock_info(args.symbol)
    spot_df = fetch_spot_snapshot(args.symbol, args.name)

    write_csv(history_df, hist_path)
    write_csv(info_df, info_path)
    write_csv(spot_df, spot_path)


if __name__ == "__main__":
    main()
