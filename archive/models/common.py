"""class Status(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Status ({}) - {}>'.format(self.id, self.name)

    @classmethod
    def getIdByName(cls, name):
        return cls.query.filter_by(name=name).first().id

    @classmethod
    def getNameById(cls, id):
        return cls.query.filter_by(id=id).first().name
"""
