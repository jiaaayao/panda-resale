import numpy as np 
import pandas as pd
import argparse 

from dotenv import dotenv_values

#fix dtypes, parse months and compute price per sqm
def clean(list_paths):
    """ 
    cats = {"town": pd.CategoricalDtype(["ANG MO KIO", "BISHAN"], ordered=False),
            "flat_type": pd.CategoricalDtype(["1 ROOM", "2 ROOM"], ordered=False),
    } 
    """
    
    #create master dataframe using list comprehension
    cleaned = pd.concat(
        [
            pd.read_csv(
                header=0,
                filepath_or_buffer=path,
                dtype={
                "town": "category",
                "flat_type": "category",
            },
            parse_dates=['month', 'lease_commence_date'],
            date_format={'month': '%Y-%m', 'lease_commence_date': '%Y'}
            ).dropna( #removes rows with empty cells
            ).assign(price_per_sqm = lambda x: (round(x["resale_price"]/x["floor_area_sqm"], 2))
            ) for path in list_paths
        ]
    )
    cleaned["flat_model"] = cleaned["flat_model"].astype("category")
    return cleaned

'''
work in progress
    r1 = r"(?P<year>[0-9][0-9]) years (?P<month>[0-9][0-9]) months"
    df = cleaned["remaining_lease"].str.extract(r1, expand=False).assign(
        remaining_lease_years = lambda x: (x['year']),
        remaining_lease_months = lambda x: (x['month']),
    )
'''

#creates master dataframe
cleaned = clean(list(dotenv_values(".env.test").values()))

def main(test = False): 
    list_paths = list((dotenv_values(".env.test") if test else dotenv_values(".env")).values())
    print("Cleaning and returning master dataframe from the following paths: ", str(list_paths))
    print(clean(list_paths))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", "-t", action="store_true")
    args = parser.parse_args()
    main(test=args.test)
    
'''
month                  datetime64[us]
town                         category
flat_type                    category
block                             str
street_name                       str
storey_range                      str
floor_area_sqm                float64
flat_model                   category
lease_commence_date    datetime64[us]
remaining_lease                object
resale_price                  float64
price_per_sqm                 float64
dtype: object
'''