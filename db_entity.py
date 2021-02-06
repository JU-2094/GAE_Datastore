import google.cloud.logging
import logging
from google.cloud import ndb

class User(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()

class Review(ndb.Model):
    text = ndb.TextProperty()
    rating = ndb.IntegerProperty()

class Location(ndb.Model):
   location = ndb.StringProperty() 
   address = ndb.TextProperty()
   category = ndb.StringProperty()
   subcategory = ndb.StringProperty(required=False)
   gpoint = ndb.GeoPtProperty(indexed=False)
   name = ndb.StringProperty()
   polarity = ndb.FloatProperty()
   review = ndb.StructuredProperty(Review, indexed=False, repeated=True, required=False)
   # review = ndb.KeyProperty(indexed=False, repeated=True, required=False) 

   @classmethod
   def get_entities(cls, fetch=10):
       return cls.query().order(cls.name, cls.polarity).fetch(10)

   @classmethod
   def get_filter_page(cls, args_f, cursor=None, fetch=10):
       cllog = google.cloud.logging.Client()
       cllog.get_default_handler()
       cllog.setup_logging()

       cur_filters = args_f
       prop_arr = [cls.location, cls.name, cls.category, 
                   cls.subcategory]
       
       logging.error("location fil="+args_f[0])
       logging.error("name fil="+args_f[1])
       logging.error("category fil="+args_f[2])
       logging.error("polarity fil="+str(args_f[-2:][0]))
       
       logging.error("QUERY (0)") 
       query = cls.query().order(-cls.polarity)
       logging.error("QUERY (1)") 

       # Can't use zip() because NoneType is not suscriptable
       for i in range (len(prop_arr)): 
           prop = prop_arr[i]
           val = args_f[i]
           if val:
               logging.error(" in apply filter for val="+val+" with i="+str(i))
               query = query.filter(prop == val)

       if args_f[-2:][0]:
           query = query.filter(cls.polarity >= args_f[-2:][0])
       if args_f[-2:][1]:
           query = query.filter(cls.polarity <= args_f[-2:][0])

       return query.fetch_page(fetch, start_cursor=cursor)

   @classmethod
   def get_cursor_page(cls, cursor=None, flg_filter=0, filters=None, fetch=10):
       if cursor:
           cursor = ndb.Cursor(urlsafe=cursor)

       if flg_filter == 0:
           data, cursor, flg = cls.query().order(-cls.polarity).fetch_page(fetch, start_cursor=cursor)
       elif flg_filter == 2: 
           data, cursor, flg = cls.query().fetch_page(fetch, start_cursor=cursor)
       else:
           data, cursor, flg = cls.get_filter_page(filters, cursor, fetch)
       return data, cursor.urlsafe(), flg

