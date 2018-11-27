#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging

# [START imports]
from flask import Flask, render_template, request,jsonify,session,redirect, url_for
from src.common.database import Database
from src.models.user import User
from src.models.admin import Admin
from src.models.readings import Readings
from src.models.directions import Directions
from bson.json_util import dumps,loads

# [END imports]

# [START create_app]
app = Flask(__name__)
app.secret_key="harsh"
# [END create_app]


@app.route('/')
def form1():
    return render_template('index1.html')

@app.route('/dashboard')
def form3(enableMaterial=True):
    users=Admin.fetchUsers(session['adminemail'])
    if enableMaterial==True:
        materials=Admin.fetchDelivery()
    else:
        materials=[]
    print(users)
    return render_template('dashboard.html',users=list(users),materials=materials)

@app.route('/canvas')
def form2():
    return render_template('canvas.html')

@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/admin_login',methods=['POST'])
def login_admin():
    email=request.form['email']
    password=request.form['pwd']

    name=Admin.login_valid(email,password)
    if  name is not None:
        Admin.login(email)
        return redirect(url_for('form3'))
    else:
        session['adminemail']=None
    print(session['adminemail'])
    return redirect(url_for('form1'))

@app.route('/logout')
def logout_admin():
    Admin.logout()
    return redirect(url_for('form1'))


@app.route('/auth/login',methods=['POST'])
def login_user():
    email=request.form['email']
    password=request.form['password']

    name=User.login_valid(email,password)
    if  name is not None:
        User.login(email)
        return jsonify(status="Success",email=email,name=name),200
    else:
        session['email']=None
        return jsonify(status="Fail",error="Invalid Credentials"),200


    return render_template("profile.html",email=session['email'])

@app.route('/auth/register',methods=['POST'])
def register_user():
#    try:
        email=request.form['email']
        password=request.form['password']
        name=request.form['name']
        if User.register(name,email,password):
        	return jsonify(status="Success",email=email),200
        else:
        	return jsonify(status="Fail",error="User Already Exists"),200
#    except:
#        return jsonify(status="Fail",error="Wrong Parameters"),400

@app.route('/sendReadings',methods=['POST'])
def push_readings():
    latitude=request.json['latitude']
    longitude=request.json['longitude']
    cartID=request.json['cartID']
    ir1=request.json['ir1']
    ir2=request.json['ir2']

    if Readings.push(cartID,latitude,longitude,ir1,ir2):
        return jsonify(status="Success"),200
    else:
        return jsonify(status="Fail"),200

@app.route('/sendDirection',methods=['POST'])
def push_directions():
    direction=request.json['direction']
    distance=request.json['distance']
    cartID=request.json['cartID']

    if Directions.push(cartID,direction,distance):
        return jsonify(status="Success"),200
    else:
        return jsonify(status="Fail"),200

@app.route('/assignDelivery',methods=['POST'])
def assign_delivery():
    user_email=request.form['user_email']
    if Admin.assignDelivery(user_email):
        return form3(False)
    else:
        return jsonify(status="Fail"),200

@app.route('/getDelivery',methods=['POST'])
def get_delivery():
    user_email=request.json['user_email']
    if User.get_delivery(user_email):
        return jsonify(status="Success",data=dumps(User.get_delivery(user_email)))
    else:
        return jsonify(status="Fail"),200

@app.route('/startCart',methods=['POST'])
def start_cart():
    cartID=request.json['cartID']
    email=request.json['email']
    prevCartID=request.json['prevCartID']
    if Directions.requestNewCart(email,prevCartID,cartID):
        return jsonify(status="Success"),200
    else:
        return jsonify(status="Fail"),200

@app.route('/stopCart',methods=['POST'])
def stop_directions():
    cartID=request.json['cartID']

    if Directions.stopCart(cartID):
        return jsonify(status="Success"),200
    else:
        return jsonify(status="Fail"),200

@app.route('/getReadings',methods=['GET'])
def get_readings():
    return jsonify(data=dumps(Readings.get()))

@app.route('/getReading/<int:cart_id>',methods=['GET'])
def get_reading(cart_id):
    return jsonify(data=dumps(Readings.getCartReading(cart_id)))

@app.route('/getDirection/<int:cart_id>',methods=['GET'])
def get_direction(cart_id):
    return jsonify(data=dumps(Directions.getCartDirections(cart_id)))

@app.route('/getPosition/<int:cart_id>',methods=['GET'])
def get_position(cart_id):
    return jsonify({"data":dumps(Directions.getCartPosition(cart_id))})

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]


#uncomment these below lines so that you word locally
if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True,host="0.0.0.0",threaded=True)