from project import db, app

def masked(data):
    if data:
        return '*' * len(data)
    return none


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
        return f"Customer(ID: {self.id}, Name: {masked(self.name)}, City: {masked(self.city)}, Age: {masked(self.age)}, Pesel: {masked(self.pesel)}, Street: {masked(self.street)}, AppNo: {masked(self.appNo)})"


with app.app_context():
    db.create_all()
