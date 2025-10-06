#app_controller.py
from flask import Flask, render_template, request, redirect, flash
from models.db import db, instance
from controllers.sensors_controller import sensor_

def create_app():
    app = Flask(__name__,
                template_folder="./views/",
                static_folder="./static/",
                root_path="./")
    
    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = instance
    db.init_app(app)
        
    app.register_blueprint(sensor_, url_prefix='/')
    
    @app.route('/')
    def index():
        return render_template("home.html")

    @app.route('/home')
    def home():
        return render_template("home.html")

    @app.route('/register_user')
    def register_user():
        return render_template("register_user.html")

    @app.route('/register_sensor')
    def register_sensor():
        return render_template("register_sensor.html")

    @app.route('/register_actuator')
    def register_actuator():
        return render_template("register_actuator.html")

    @app.route('/list_users')
    def list_users():
        return render_template("users.html")

    @app.route('/sensors')
    def sensors():
        return render_template("sensors.html")

    @app.route('/actuators')
    def actuators():
        return render_template("actuators.html")

    @app.route('/tempo_real')
    def tempo_real():
        values = {'temperature': 25, 'humidity': 60}
        return render_template("tr.html", values=values)

    @app.route('/publish')
    def publish():
        return render_template("publish.html")

    @app.route('/history_read')
    def history_read():
        sensors = [{'id': 1}, {'id': 2}, {'id': 3}]
        return render_template("history_read.html", sensors=sensors)

    @app.route('/history_write')
    def history_write():
        actuators = [{'id': 1}, {'id': 2}, {'id': 3}]
        return render_template("history_write.html", actuators=actuators)

    @app.route('/get_read', methods=['POST'])
    def get_read():
        sensor_id = request.form['id']
        start = request.form['start']
        end = request.form['end']
        sensors = [{'id': 1}, {'id': 2}, {'id': 3}]
        read = [
            {'sensors_id': sensor_id, 'value': 25.5, 'read_datetime': '2023-01-01 12:00:00'},
            {'sensors_id': sensor_id, 'value': 26.0, 'read_datetime': '2023-01-01 13:00:00'},
        ]
        return render_template("history_read.html", sensors=sensors, read=read)

    @app.route('/get_write', methods=['POST'])
    def get_write():
        actuator_id = request.form['id']
        start = request.form['start']
        end = request.form['end']
        actuators = [{'id': 1}, {'id': 2}, {'id': 3}]
        write = [
            {'actuators_id': actuator_id, 'value': 1, 'write_datetime': '2023-01-01 12:00:00'},
            {'actuators_id': actuator_id, 'value': 0, 'write_datetime': '2023-01-01 13:00:00'},
        ]
        return render_template("history_write.html", actuators=actuators, write=write)

    @app.route('/validated_user', methods=['POST'])
    def validated_user():
        email = request.form['email']
        password = request.form['password']
        if email == 'usuario1@gmail.com' and password == '1234':
            return redirect('/home')
        else:
            flash('Credenciais inválidas')
            return redirect('/login')

    @app.route('/logoff')
    def logoff():
        return redirect('/login')

    @app.route('/login')
    def login():
        return render_template("login.html")

    return app

