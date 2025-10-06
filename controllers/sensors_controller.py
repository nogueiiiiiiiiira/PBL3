from flask import Blueprint, request, render_template, redirect, url_for
from models.iot.sensors import Sensor
sensor_ = Blueprint("sensor_", __name__ , template_folder="views")

@sensor_.route('/register_sensor')

def register_sensor():
    return render_template("register_sensor.html")

@sensor_.route('/add_sensor', methods=['POST'])
def add_sensor():
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = True if request.form.get("is_active") == "on" else False
    Sensor.save_sensor(name, brand, model, topic, unit, is_active )
    return render_template("home.html")

@sensor_.route('/sensors')
def sensors():
    sensors = Sensor.get_sensors()
    return render_template("sensors.html", sensors = sensors)
