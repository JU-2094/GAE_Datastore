import pandas as pd
import random
from google.cloud import ndb
from db_entity import Review, Location

def insert(cls, dataframe):
    with cls.context():
        for row in dataframe.itertuples():
            try:
                p_rev = Review(text = str(row.reviews), rating = random.randint(1,5))
                p_rev.put()
                p_loc = Location(
                        location = str(row.location),
                        name = str(row.name),
                        address = str(row.address),
                        category = str(row.category),
                        subcategory = str(row.subCategory),
                        polarity = round(random.uniform(1,5),1),
                        lat = float(row.lat),
                        lng = float(row.lng),
                        review = [p_rev.key] 
                        )
                p_loc.put()
            except:
                print("one row failed")


def main():
    client = ndb.Client()
    
    # only insert 1500 because the rest of the rows are not completed
    df = pd.read_csv('data/paris-attraction.csv')
    insert(client, df[0:200])
    
    df = pd.read_csv('data/paris-poi.csv')
    insert(client, df[0:200])

    df = pd.read_csv('data/amsterdam-attraction.csv')
    insert(client, df[0:200])

if __name__ == "__main__":
    main()
    print("end of insertions")

