from models.db import db
from models.iot.devices import Device

class Sensor(db.Model):
    __tablename__ = 'sensors'
    id= db.Column('id', db.Integer, primary_key=True)
    devices_id = db.Column( db.Integer, db.ForeignKey(Device.id))
    unit = db.Column(db.String(50))
    topic = db.Column(db.String(50))

    def save_sensor(cls, name, brand, model, topic, unit, is_active):
        device = Device(name=name, brand=brand, model=model, is_active=is_active)
        db.session.add(device)
        db.session.commit()
        sensor = cls(devices_id=device.id, topic=topic, unit=unit)
        db.session.add(sensor)
        db.session.commit()

    def get_sensors():
        sensors = Sensor.query.join(Device, Device.id == Sensor.devices_id)\
        .add_columns(Device.id, Device.name,
        Device.brand, Device.model,
        Device.is_active, Sensor.topic,
        Sensor.unit).all()
        
        return sensors



