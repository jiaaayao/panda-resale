import datetime as dt
import argparse
from clean import cleaned, clean

def group_by_town(df, town_name):
    #validation
    if town_name not in df.town.cat.categories.values:
        raise ValueError("Given town name is not in list of valid town names")
    return df[df["town"] == town_name]

def filter_by_towns(df, town_list: list):
    return df[df["town"].isin(town_list)]

def group_by_flat_type(df, flat_type):
    if flat_type not in df.flat_type.cat.categories.values:
        raise ValueError("Given flat type is not valid")
    return df[df["flat_type"] == flat_type]

def filter_by_flat_type(df, flat_type_list: list):
    return df[df["flat_type"].isin(flat_type_list)]

def group_by_year(df, year: int):
    return df[df.month.dt.year == year]

#compares month column of df against a tuple of two datetime.date objects which functions as a range
def filter_by_date(df, date_range: tuple):
    return df[(df["month"].dt.date >= date_range[0]) & (df["month"].dt.date <= date_range[1])]

def main(test = False):
    if test:
        cleaned = clean(["data/test data.csv"])
    print(filter_by_towns(cleaned, ["ANG MO KIO"]))    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", "-t", action="store_true")
    args = parser.parse_args()
    main(test=args.test)