from project import db, app


def _mask(value, visible=0):
    """Replace all but the last `visible` characters with '*', keeping the length."""
    if value is None:
        return None
    s = str(value)
    return "*" * (len(s) - visible) + (s[-visible:] if visible else "")


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

    def __init__(self, name, city, age, pesel, street, appNo):
        self.name = name
        self.city = city
        self.age = age
        self.pesel = pesel
        self.street = street
        self.appNo = appNo
        print("Getting: " + str(self),flush=True)

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age}, Pesel: {_mask(self.pesel)}, Street: {_mask(self.street)}, AppNo: {_mask(self.appNo)})"


with app.app_context():
    db.create_all()
