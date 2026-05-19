from flask import Flask, render_template, url_for, request, redirect, session, jsonify
from .modele import *
import uuid,os, json, requests
app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_pyfile('config.py')

@app.route('/')
def index():

    hasShower = False
    hasDisabledAccess = False
    hasChangingRoom = False
    hasLuxury = False
    distance = 50000

    if 'filter_distance' in session: distance = session['filter_distance']
    if 'filter_shower' in session and session['filter_shower']: hasShower = True
    if 'filter_disabled_access' in session and session['filter_disabled_access']: hasDisabledAccess = True
    if 'filter_changing_room' in session and session['filter_changing_room']: hasChangingRoom = True
    if 'filter_luxury' in session and session['filter_luxury']: hasLuxury = True

    return render_template('index.html', hasShower = hasShower, hasDisabledAccess = hasDisabledAccess, hasChangingRoom = hasChangingRoom, hasLuxury = hasLuxury, distance = distance)

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    message = request.args.get('msg')
    if message is None:
        message = ""
    return render_template('login.html', msg = message)

@app.route('/login/submit', methods=['POST'])
def login_submit():

    user = log_in(request.form['username'], request.form['password'])
    if(len(user) != 0):
        session['ID'] = user[0][0]
        session['name'] = request.form['username']
        session['isHost'] = user[0][5]
        print(session['isHost'])

        return redirect(url_for('index'))
    
    return redirect(url_for('login', msg = "Wrong username or password"))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    message = request.args.get('msg')
    if message is None:
        message = ""
    return render_template('signup.html', msg = message)

@app.route('/signup/submit', methods=['POST'])
def signup_submit():
    # TODO

    UUID = uuid.uuid4()
    if(addUser(UUID, request.form['username'], request.form['name'], request.form['phone'], request.form['password'])):
        session['ID'] = UUID
        session['name'] = request.form['username']
        session['isHost'] = False
        return redirect(url_for('index'))

    return redirect(url_for('signup', msg = "An account si already associated with this phone number"))

@app.route('/profile')
def profile():
    if('ID' not in session):
        return redirect(url_for('login', msg = "You need to be logged in"))

    return render_template('profile.html', selected = 'profile')

@app.route('/become/a/host')
def become_a_host():
    if('ID' not in session):
        return redirect(url_for('login', msg = "You need to be logged in"))
    
    if(session['isHost'] or get_bank_id(session['ID']) != None):
        return redirect(url_for('new_thron'))
    
    return render_template('bank.html')

@app.route('/bank/submit', methods=['POST'])
def bank_submit():
    if('ID' not in session):
        return redirect(url_for('login', msg = "You need to be logged in"))
    
    if(session['isHost'] or get_bank_id(session['ID']) != []):
        return redirect(url_for('new_thron'))
    
    card_number = request.form.get('card_number')
    expiration_date = request.form.get('expiration_date')
    cvv = request.form.get('cvv')

    add_bank_id(session['ID'], card_number, expiration_date, cvv)

    return redirect(url_for('new_thron'))

@app.route('/thron/new')
def new_thron():
    if('ID' not in session):
        return redirect(url_for('login', msg = "You need to be logged in"))
    
    return render_template('new_thron.html', selected = 'throns')

@app.route('/thron/new/submit', methods=['POST'])
def new_thron_submit():
    
    if('ID' not in session):
        return redirect(url_for('login', msg = "You need to be logged in"))
    
    street = request.form.get('street')
    city = request.form.get('city')
    zipcode = request.form.get('zipcode')
    country = request.form.get('country')
    adress = street + ", " + city + ", " + zipcode + ", " + country

    if(doesBathroomExists(adress)):
        return redirect(url_for('new_thron', msg = "A bathroom already exisst at this address"))

    hasShower = booleanConvert(request.form.get('hasShower'))
    hasDisabledAccess = booleanConvert(request.form.get('hasDisabledAccess'))
    hasChangingRoom = booleanConvert(request.form.get('hasChangingRoom'))
    hasLuxury = booleanConvert(request.form.get('hasLuxury'))

    uid = uuid.uuid4()
    lat, lon = getCoords(street, city, zipcode, country)


    if(addHost(uid, session['ID'], adress, lat, lon, hasShower, hasDisabledAccess, hasChangingRoom, hasLuxury)):
        session['isHost'] = True

    return redirect(url_for('my_throns'))

@app.route('/my/throns')
def my_throns():
    if('ID' not in session):
        return redirect(url_for('login', msg = "You need to be logged in"))
    
    if(not session['isHost']):
        return redirect(url_for('new_thron'))

    bathrooms = getBathrooms(session['ID'])


    return render_template('my_throns.html', bathrooms = bathrooms, selected = 'throns')

@app.route('/about')
def about():
    # TODO
    return render_template('index.html')

@app.route('/subscribtions')
def subscribtions():
    # TODO
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search():
    session['filter_distance'] = request.form.get('distance')
    session['filter_shower'] = booleanConvert(request.form.get('hasShower'))
    session['filter_disabled_access'] = booleanConvert(request.form.get('hasDisabledAccess'))
    session['filter_changing_room'] = booleanConvert(request.form.get('hasChangingRoom'))
    session['filter_luxury'] = booleanConvert(request.form.get('hasLuxury'))

    return redirect(url_for('index'))

@app.route('/api/markers')
def get_markers():

    lat, lon = geolocate()

    toilets = getToilets()

    hasShower = False
    hasDisabledAccess = False
    hasChangingRoom = False
    hasLuxury = False
    distance = 50000

    if 'filter_distance' in session: distance = session['filter_distance']
    if 'filter_shower' in session and session['filter_shower']: hasShower = True
    if 'filter_disabled_access' in session and session['filter_disabled_access']: hasDisabledAccess = True
    if 'filter_changing_room' in session and session['filter_changing_room']: hasChangingRoom = True
    if 'filter_luxury' in session and session['filter_luxury']: hasLuxury = True

    data = {
        "center": [lat, lon],
        "markers": toilets,
        "distance": distance,
        "hasShower": hasShower,
        "hasDisabledAccess": hasDisabledAccess,
        "hasChangingRoom": hasChangingRoom,
        "hasLuxury": hasLuxury
    }

    return jsonify(data)

@app.route('/api/markers/my')
def get_my_markers():
    bathrooms = getBathrooms(session['ID'])

    data = {
        "center": [bathrooms[0][3], bathrooms[0][4]],
        "markers": bathrooms
    }

    return jsonify(data)

def geolocate():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()["ip"]
    url = 'https://ipinfo.io/' + ip_address + '/json'
    r = requests.get(url)
    lat = 45.166672
    lon = 5.71667
    if(r.status_code == 200):
        j = json.loads(r.text)
        lat = j["loc"].split(',')[0]
        lon = j["loc"].split(',')[1]
    
    return lat, lon

def getCoords(street, city, zipcode, country):
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    response = requests.get('https://nominatim.openstreetmap.org/search?street=' + street + '&city=' + city + '&postalcode=' + zipcode + '&country=' + country + '&format=json', headers=headers)
    if(response.status_code != 200):
        print(response.status_code)
        return None

    data = response.json()

    if(len(data) == 0):
        return None

    print(data)
    return data[0]["lat"], data[0]["lon"]

def booleanConvert(value):
    if(value == "on"):
        return True
    else:
        return False