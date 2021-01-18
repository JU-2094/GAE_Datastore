from google.cloud import ndb

class User(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()

class Review(ndb.Model):
    text = ndb.TextProperty()
    rating = ndb.IntegerProperty()
    user = ndb.KeyProperty(indexed=False, required=False)

    @classmethod
    def get_review(cls):
        return cls.query()

    @classmethod
    def filter_rank(cls, minv, maxv):
        return cls.query().filter(AND(cls.rating >= minv,
                                      cls.rating <= maxv))

class Location(ndb.Model):
   location = ndb.StringProperty() 
   address = ndb.TextProperty()
   category = ndb.StringProperty()
   subcategory = ndb.StringProperty(required=False)
   lat = ndb.FloatProperty(indexed=False)
   lng = ndb.FloatProperty(indexed=False)
   name = ndb.StringProperty()
   polarity = ndb.FloatProperty()
   review = ndb.KeyProperty(indexed=False, repeated=True, required=False) 

   @classmethod
   def get_entities(cls, fetch=10):
       return cls.query().order(cls.name, cls.polarity).fetch(10)

   @classmethod
   def get_filter_page(cls, args_f, cursor=None, fetch=10):
       cur_filters = args_f
       prop_arr = [cls.location, cls.name, cls.category, 
                   cls.subcategory]
       query = cls.query().order(-cls.polarity)

       # Can't use zip() because NoneType is not suscriptable
       for i in range (len(prop_arr)): 
           prop = prop_arr[i]
           val = args_f[i]
           if val: 
               query = query.filter(prop == val)
       
       if args_f[-2:][0]:
           query = query.filter(cls.polarity >= args_f[-2:][0])
       if args_f[-2:][1]:
           query = query.filter(cls.polarity <= args_f[-2:][0])

       return query.fetch_page(fetch, start_cursor=cursor)

   @classmethod
   def get_cursor_page(cls, cursor, flg_filter, filters, fetch=10):
       if flg_filter == 0:
           return cls.query().order(-cls.polarity).fetch_page(fetch, start_cursor=cursor)
       return cls.get_filter_page(filters, cursor, fetch)

