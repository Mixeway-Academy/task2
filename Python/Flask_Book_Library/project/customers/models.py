from project import db, app

def mask_value(val):
    if not val:
        return val
    return '*' * len(str(val))

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
        masked_pesel = mask_value(self.pesel)
        masked_street = mask_value(self.street)
        masked_city = mask_value(self.city)
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {masked_city}, Age: {self.age}, Pesel: {masked_pesel}, Street: {masked_street}, AppNo: {self.appNo})"


with app.app_context():
    db.create_all()
