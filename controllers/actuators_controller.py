from flask import Blueprint, request, render_template, redirect, url_for
from models.iot.actuators import Actuator
actuator_ = Blueprint("actuator_", __name__ , template_folder="views")

@actuator_.route('/register_actuator')

def register_actuator():
    return render_template("register_actuator.html")

@actuator_.route('/add_actuator', methods=['POST'])
def add_actuator():
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = True if request.form.get("is_active") == "on" else False
    Actuator.save_actuator(name, brand, model, topic, unit, is_active )
    return render_template("home.html")

@actuator_.route('/actuators')
def actuators():
    actuators = Actuator.get_actuators()
    return render_template("actuators.html", actuators = actuators)

