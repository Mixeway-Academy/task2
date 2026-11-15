from project import db, app


# Customer model
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    city = db.Column(db.String(64))
    age = db.Column(db.Integer)
    pesel = db.Column(db.String(64))
    street = db.Column(db.String(128))
    appNo = db.Column(db.String(10))

    def _mask(self, value):
        if value is None:
            return None
        return '***'    # constant number of characters

    def __init__(self, name, city, age, pesel, street, appNo):
        self.name = name
        self.city = city
        self.age = age
        self.pesel = pesel
        self.street = street
        self.appNo = appNo
        print("Getting: " + str(self),flush=True)

    def __repr__(self):
        # Name is not masked in order to allow identification in logs
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self._mask(self.city)}, Age: {self._mask(self.age)}, Pesel: {self._mask(self.pesel)}, Street: {self._mask(self.street)}, AppNo: {self._mask(self.appNo)})"


with app.app_context():
    db.create_all()
