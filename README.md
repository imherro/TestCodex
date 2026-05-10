# TestCodex

AKShare 示例：获取邮储银行 A 股（股票代码：`601658`）的全部可用股票数据，并保存为 CSV。

## 数据内容

脚本会输出到 `data/` 目录：

- `psbc_601658_hist_daily_none.csv`：历史行情数据，默认日频、不复权、全量可用区间
- `psbc_601658_info.csv`：个股基本信息
- `psbc_601658_spot.csv`：当前 A 股行情快照

历史行情接口使用 AKShare 的 `stock_zh_a_hist`。根据 AKShare 文档，该接口支持 `daily`、`weekly`、`monthly`，并支持不复权、前复权 `qfq`、后复权 `hfq`。

## 安装

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

macOS / Linux 激活虚拟环境：

```bash
source .venv/bin/activate
```

## 运行

默认获取邮储银行 A 股全部可用日线数据：

```bash
python src/fetch_psbc_a_stock.py
```

指定日期、周期、复权方式：

```bash
python src/fetch_psbc_a_stock.py --start-date 20191210 --end-date 20260510 --period daily --adjust qfq
```

只保存到指定目录：

```bash
python src/fetch_psbc_a_stock.py --output-dir output
```

## 参数说明

- `--symbol`：股票代码，默认 `601658`
- `--name`：股票名称，默认 `邮储银行`
- `--start-date`：开始日期，格式 `YYYYMMDD`，默认 `19700101`
- `--end-date`：结束日期，格式 `YYYYMMDD`，默认 `20500101`
- `--period`：周期，可选 `daily`、`weekly`、`monthly`
- `--adjust`：复权方式，可选空字符串、不复权；`qfq` 前复权；`hfq` 后复权
- `--output-dir`：输出目录，默认 `data`

## 注意

AKShare 数据来自第三方公开数据源，接口和字段可能随数据源变化。若运行时报网络或字段错误，先升级 AKShare：

```bash
pip install -U akshare
```
