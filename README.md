# Panda Resale: HDB Resale Price Explorer

An interactive tool for exploring Singapore HDB resale flat prices. It loads one or more HDB resale CSV files, cleans them with pandas, and shows the transactions in a Streamlit app where you can filter by town, flat type and date range.

## Features

- Loads and combines multiple HDB resale CSV files into one cleaned dataset
- Adds a `price_per_sqm` column (resale price divided by floor area)
- Filter functions for town, flat type, year and date range (`analysis.py`)
- Interactive scatter plot of resale price over time, coloured by town, with flat type and flat model shown on hover (`app.py`)

## Project structure

| File | Purpose |
|---|---|
| `clean.py` | Reads the CSV files listed in `.env`, fixes data types, parses dates, drops incomplete rows and computes `price_per_sqm`. Exposes the result as `cleaned`. |
| `analysis.py` | Reusable filtering functions: `group_by_town`, `filter_by_towns`, `group_by_flat_type`, `filter_by_flat_type`, `group_by_year`, `filter_by_date`. |
| `app.py` | The Streamlit app: sidebar filters, date slider and Plotly chart. |
| `.env` | Lists the paths of your data files (you create this). |
| `.env.test` | Lists the paths of test data files, used by `clean.py --test` (optional). |
| `data/` | Folder for your CSV files. |

## Requirements

- Python 3.9 or newer
- `pandas` (2.0 or newer)
- `streamlit` (a recent version, as the app uses `select_all` on its multiselects)
- `plotly`
- `python-dotenv`

Install them with:

```
pip install pandas streamlit plotly python-dotenv
```

## Setup

### 1. Add your data

Put your HDB resale CSV files in the `data/` folder (for example, the HDB resale flat prices datasets from data.gov.sg). Each file needs these columns:

`month`, `town`, `flat_type`, `block`, `street_name`, `storey_range`, `floor_area_sqm`, `flat_model`, `lease_commence_date`, `resale_price`

- `month` must be formatted as `YYYY-MM` and `lease_commence_date` as `YYYY`.
- Rows with any empty cell are dropped during cleaning.
- A `remaining_lease` column is optional.

### 2. Create a `.env` file

In the project folder, create a file called `.env` with one line per data file. The names on the left can be anything. Only the paths on the right are used.

```
DATA_1=data/first_file.csv
DATA_2=data/second_file.csv
```

`.env` is read every time `clean.py` is imported, so it must exist before you run any of the scripts.

### 3. (Optional) Set up test data

To try the code on a small sample, put `test data.csv` in the `data/` folder. For `clean.py --test`, create a `.env.test` file in the same format as `.env`:

```
TEST_DATA=data/test data.csv
```

## Usage

### Run the app

```
streamlit run app.py
```

This opens the explorer in your browser:

1. Use the **Towns** and **Flat Type** boxes in the sidebar to choose what to show (everything is selected by default).
2. Drag the date slider to limit the months shown.
3. Hover over a point to see its flat type and flat model.

### Check the cleaned data

```
python clean.py
python clean.py --test
```

This prints the cleaned dataframe and its column types. With `--test`, it reads the paths from `.env.test` instead of `.env`.

### Try the filters

```
python analysis.py --test
```

This loads `data/test data.csv` and prints the rows for Ang Mo Kio as a demonstration.

You can also use the filters in your own code:

```python
from clean import cleaned
from analysis import filter_by_towns, filter_by_flat_type, filter_by_date
import datetime as dt

subset = filter_by_date(
    filter_by_flat_type(
        filter_by_towns(cleaned, ["BEDOK", "TAMPINES"]),
        ["4 ROOM", "5 ROOM"],
    ),
    (dt.date(2013, 1, 1), dt.date(2014, 12, 1)),
)
```

## How the cleaning works

1. Each file in the list is read with `month` and `lease_commence_date` parsed as dates.
2. Rows with empty cells are removed.
3. `price_per_sqm` is added, rounded to 2 decimal places.
4. All files are combined into one dataframe.
5. `town`, `flat_type` and `flat_model` are converted to categories, which the app uses to build its filter options.