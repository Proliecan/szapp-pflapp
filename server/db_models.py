from datetime import datetime
from server import db, ma

# -----------------------------------------
# DataBase configuration 
# TODO: finish DB
# https://www.youtube.com/watch?v=cYWiDiIUxQc
# https://www.youtube.com/watch?v=44PvX0Yv368

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_file = db.Column(db.String(), unique=False, nullable=False, default='static/img/001-botanic.svg')
    min_fill_value = db.Column(db.Integer, unique=False, nullable=False, default=0)
    max_fill_value = db.Column(db.Integer, unique=False, nullable=False, default=5)
    values = db.relationship('WaterlevelData', backref='name', lazy=True)

    def __repr__(self) -> str:
        return f"TESTPlant('{self.name}', '{self.creation_date}', '{self.last_update}', '{self.image_file}')"

class WaterlevelData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'), nullable=False)
    value = db.Column(db.Integer, nullable=False, default=2)
    report_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Plant('{self.value}', '{self.report_time}')"

class PlantSchema(ma.SQLAlchemyAutoSchema):
      class Meta:
            model = Plant
            load_instance = True
