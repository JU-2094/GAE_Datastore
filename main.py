# [START gae_python38_app]
# [START gae_python3_app]
from flask import Flask, render_template, request, redirect, url_for, flash
from google.cloud import ndb
from db_entity import User, Review, Location

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
client = ndb.Client()
gdata = []
gfilt = []

@app.route('/')
def index(cursor=None):
    data = []
    with client.context():
        entities, cursor, flg = Location.get_cursor_page(cursor,0,None)
        data.extend(entities)
    gdata = data
    return render_template('index.html', item_list_loc=data, cursor_ptr=cursor)

@app.route('/add_location', methods=['POST'])
def add_location():
    if request.method == 'POST':
        loc = str(request.form['form_location'])
        locnam = str(request.form['form_name'])
        locadd = str(request.form['form_address'])
        locpol = float(request.form['form_polarity'])
        loccat = str(request.form['form_category'])
        locsub = str(request.form['form_subcategory'])
        loclat = float(request.form['form_lat'])
        loclng = float(request.form['form_lng'])

        with client.context():
            ptr = Location(
                    location = loc,
                    name = locnam,
                    address = locadd,
                    category = loccat,
                    subcategory = locsub,
                    polarity = locpol,
                    lat = loclat,
                    lng = loclng)
            ptr.put()
        return redirect(url_for('index'))

# To add a review we need a reference of the location that was clicked
@app.route('/add_review/<obj_pos>', methods=['POST'])
def add_review(obj_pos):
    if request.method == 'POST':
        with client.context():
            rev = Review(text=str(request.form['form_text']), 
                         rating= int(request.form['form_rating'])
                         )
            rev.put()
            loc = gdata[obj_pos].key.get()
            loc.review.append(rev.key)
            loc.put()
    return redirect(url_for('index')) 

@app.route('/edit/<obj_pos>', methods=['POST'])
def edit_user(obj_pos):
    if request.method == 'POST':
        with client.context():
            ob_loc = gdata[obj_pos].key.get()
            loc = request.form['form_location']
            locnam = request.form['form_name']
            locadd = request.form['form_address']
            locpol = request.form['form_polarity']
            loccat = request.form['form_category']
            locsub = request.form['form_subcategory']
            loclat = request.form['form_lat']
            loclng = request.form['form_lng'] 
            if loc:
                obj_loc.location = loc
            if locnam:
                obj_loc.name = locnam
            if locadd:
                obj_loc.address = locadd
            if locpol:
                obj_loc.polarity = float(locpol)
            if loccat:
                obj_loc.category = loccat
            if locsub:
                obj_loc.subcategory = locsub
            if loclat:
                obj_loc.lat = float(loclat)
            if loclng:
                obj_loc.lng = float(loclng)
            ob_loc.put()
    return redirect(url_for('index'))

@app.route('/apply_filter', methods=['POST'])
def apply_filter():
    data = []
    pol_min = None
    pol_max = None
    if request['pol_min']:
       pol_min = float(request['pol_min'])
    if request['pol_max']:
       pol_max = float(request['pol_min'])
    filters = [request['loc_f'], request['name_f'],
               request['cat_f'], request['subcat'],
               pol_min, pol_max]
    gfilt = filters
    with client.context():
        try:
            entities, cursor, flg = Location.get_filter_page(filters, cursor)
            data.extend(entities)
        except:
            # Should log that the operation is not supported
            # i.e. all filters enabled including name
            data = []
    gdata = data
    return render_template('index.html', item_list_loc=data, cursor_ptr=cursor)
    #return redirect(url_for('index', item_list_loc=data, cursor_ptr=cursor))


@app.route('/next_page/<cursor>/<flg>')
def next_page(cursor, flg_filter):
    data = []
    with client.context():
         entities, cursor, flg = Location.get_cursor_page(cursor, flg_filter, gfilt)
         data.extend(entities)
    gdata = data
    # return redirect(url_for('index', item_list_loc=data, cursor_ptr=cursor))
    return render_template('index.html', item_list_loc=data, cursor_ptr=cursor)

@app.route('/delete/<obj_pos>')
def delete_user(obj_pos):
    with client.context():
        gdata[obj_pos].key.delete()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_app]
# [END gae_python38_app]
