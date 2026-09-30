import pandas as pd
import sys
from clean import cleaned

def group_by_town(df, town_name):
    #validation
    if town_name not in df.town.cat.categories.values:
        raise ValueError("Given town name is not in list of valid town names")
    return df[df["town"] == town_name]

def group_by_flat_type(df, flat_type):
    if flat_type not in df.flat_type.cat.categories.values:
        raise ValueError("Given flat type is not valid")
    return df[df["flat_type"] == flat_type]

def group_by_year(df, year: int):
    return df[df.month.dt.year == year]

def main():
    print(group_by_year(cleaned, int(sys.argv[1])))

if __name__ == "__main__":
    main()