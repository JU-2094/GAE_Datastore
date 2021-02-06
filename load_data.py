import pandas as pd
import random
import requests
from google.cloud import ndb
from db_entity import Review, Location

@ndb.transactional_async
def insert(cls, dataframe):
    with cls.context():
        for row in dataframe.itertuples():
            try:
                p_loc = Location(
                        location = str(row.location),
                        name = str(row.name),
                        address = str(row.address),
                        category = str(row.category),
                        subcategory = str(row.subCategory),
                        polarity = round(random.uniform(1,5),1),
                        gpoint = ndb.GeoPt(float(row.lat), float(row.lng))
                        )
                
                url_raw = requests.get(row.reviews)
                data_rev = url_raw.json()
                i = 0
                for rev in data_rev:
                    if (i>=10):
                        break
                    p_loc.review.append(Review(text = rev['text'],
                                               rating = int(rev['polarity']%6)))
                    i = i+1

                p_loc.put()
            except:
                print("one row failed")

def main():
    client = ndb.Client()
    
    # only insert 1500 because the rest of the rows are not completed
    df = pd.read_csv('data/paris-attraction.csv')
    #insert(client, df[0:100])
    
    #df = pd.read_csv('data/paris-poi.csv')
    #insert(client, df[0:100])

    #df = pd.read_csv('data/amsterdam-attraction.csv')
    #insert(client, df[0:100])
    
    #df = pd.read_csv('data/barcelona-attraction.csv')
    #insert(client, df[0:100])

    #df = pd.read_csv('data/rome-poi.csv')
    #insert(client, df[0:100])

if __name__ == "__main__":
    main()
    print("end of insertions")

