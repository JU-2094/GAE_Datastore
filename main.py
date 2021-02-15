# [START gae_python38_app]
# [START gae_python3_app]
import google.cloud.logging
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session
from google.cloud import ndb
from db_entity import User, Review, Location
import copy
# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
app.secret_key = 'clave_de_prueba'

client = ndb.Client()

clientlog = google.cloud.logging.Client()
clientlog.get_default_handler()
clientlog.setup_logging()

gdata = []

@app.route('/')
def index():
    with client.context():
        data, cursor, flg = Location.get_cursor_page()
    gdata.clear()
    gdata.extend(data)
    logging.info("START OF APPLICATION DEBUG INFO");

    session['cur_list'] = [None, cursor]
    session['cur_idx'] = 0
    session['flg_filter'] = 0
    session['gfilt'] = []

    return render_template('index.html', len = len(data), dataList = data)

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
                    gpoint = ndb.GeoPt(loclat, loclng)
                    )
            ptr.put()
        return redirect(url_for('index'))

# To add a review we need a reference of the location that was clicked
@app.route('/add_review/<obj_pos>', methods=['POST'])
def add_review(obj_pos):
    if request.method == 'POST':
        with client.context():
            # rev = Review(text=str(request.form['form_text']), 
            #             rating= int(request.form['form_rating'])
            #             )
            # rev.put()
            rowToChange = int(obj_pos)
            loc = gdata[rowToChange].key.get()
            json_data = request.json
            if not json_data:
                return "", 202 

            text = json_data['reviewText']
            rating = json_data['reviewRating']
    
            # loc.review.append(rev.key)
            loc.review.append(Review(text=str(text),
                                            rating=int(rating)))
            loc.put()
            logging.warning("DEBUG: obj_pos="+str(obj_pos))
            logging.warning("DEBUG: len(gdata)="+str(len(gdata)))
    return "Review added", 202

@app.route('/apply_filter')
def apply_filter():
    # if request.method == 'POST':
    if 1:
        data = []
        pol_min = None
        pol_max = None
        
        logging.error("APPLY FILTER function")

        if request.args.get('pol_min'):
           pol_min = float(request.args.get('pol_min'))
        if request.args.get('pol_max'):
           pol_max = float(request.args.get('pol_max'))
        filters = [request.args.get('loc_f'), request.args.get('name_f'),
                   request.args.get('cat_f'), request.args.get('subcat_f'),
                   pol_min, pol_max]

        logging.error("filters[0]="+str(filters[0]))
        logging.error("filters[1]="+str(filters[1]))
        logging.error("filters[2]="+str(filters[2]))
        logging.error("filters[3]="+str(filters[3]))
        logging.error("filters[4]="+str(filters[4]))
        logging.error("filters[5]="+str(filters[5]))
        with client.context():
            logging.error("IN CONTEXT APPLY FILTER")
            #data, cursor, flg = Location.get_cursor_page(flg_filter=1, filters=filters)
            try: 
                data, cursor, flg = Location.get_cursor_page(flg_filter=1, filters=filters)
                logging.error("QUERY PASSED")
                logging.error("LEN of data ="+str(len(data)))
            except:
                logging.error("FAILED TO DO QUERY")
                data = []
            logging.error("END OF APPLY FILTER")
       

        session['flg_filter'] = 1
        session['gfilt'].clear()
        session['gfilt'].extend(filters)

        gdata.clear()
        gdata.extend(data)
        
        logging.error("len data="+str(len(data)))
        # logging.error("first row location ="+data[0].location)
        logging.error("END of FILTER function")

    #return redirect(url_for('index', item_list_loc=data, cursor_ptr=cursor))
    return render_template('index.html', len = len(data), dataList = data)
    # return render_template('test.html')
    #return redirect(url_for('index', len = len(data), dataList = data))
    # return gdata, 202
    # return {'len':len(data), 'dataList':data}, 202
    # return data, 202

@app.route('/edit/<obj_pos>', methods=['POST'])
def update_row(obj_pos):
    if request.method == 'POST':
        with client.context():
            rowToChange = int(obj_pos)
            obj_loc = gdata[rowToChange].key.get()
            json_data = request.json
            if not json_data:
                # return redirect(url_for('index'))
                return "", 202 
            loc = json_data['location']
            locnam = json_data['name']
            locadd = json_data['address']
            locpol = json_data['polarity']
            loccat = json_data['category']
            locsub = json_data['subcategory']
            loclat = json_data['lat']
            loclng = json_data['lng']
            
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
            if loclat and loclng:
                obj_loc.gpoint = ndb.GeoPt(float(loclat), float(loclng)) 
            
            obj_loc.put()
            print(gdata)
    return "", 202

@app.route('/next_page')
def next_page():
    logging.error("NEXT_PAGE execution")
    cur_list =  session['cur_list']
    cur_idx = session['cur_idx']
    gfilt = session['gfilt']
    flg_filter = session['flg_filter']

    # end of pages
    if (len(cur_list) == (cur_idx + 1)):
       return "End of pages", 202
    cur_idx = cur_idx +1
    
    cursor = cur_list[cur_idx]

    if cursor == None:
       return "End of pages", 202
  
    with client.context():    
        logging.error("next_page getting cursor")
        data, cursor, flg = Location.get_cursor_page(cursor, flg_filter, gfilt)
        gdata.clear()
        gdata.extend(data)
        logging.error("end of query")

    if (len(cur_list) == (cur_idx+1)):
        if flg:
            session['cur_list'].append(cursor)

    session['cur_idx'] = cur_idx

    logging.error("before doing redirect or render")
    # return redirect(url_for('index', len = len(data), dataList =data))
    return render_template('index.html', len = len(data), dataList = data)
    # return "", 202

@app.route('/prev_page')
def prev_page():
    cur_list =  session['cur_list']
    cur_idx = session['cur_idx']
    gfilt = session['gfilt']
    flg_filter = session['flg_filter']

    if (cur_idx > 0):
        # position 0 is query with cursor=none
        cur_idx = cur_idx - 1
        cursor = cur_list[cur_idx]
        with client.context():
            data, cursor, flg = Location.get_cursor_page(cursor, flg_filter, gfilt)
        gdata.clear()
        gdata.extend(data)

        session['cur_idx'] = cur_idx

    return render_template('index.html', len = len(gdata), dataList = gdata)

@app.route('/delete/<obj_pos>')
def delete_user(obj_pos):
    with client.context():
        gdata[obj_pos].key.delete()
    return "", 202
   # return redirect(url_for('index'))

@app.route('/get_review/<obj_pos>')
def get_review(obj_pos):
    data = []
    return data, 202

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_app]
# [END gae_python38_app]
