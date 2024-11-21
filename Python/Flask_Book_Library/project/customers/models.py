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

    def __init__(self, name, city, age, pesel, street, appNo):
        self.name = name
        self.city = city
        self.age = age
        self.pesel = pesel
        self.street = street
        self.appNo = appNo
        print("Getting: " + str(self),flush=True)

    def __repr__(self):
        masked_pesel = '*' * len(self.pesel)
        masked_city = '*' * len(self.city)
        masked_street = '*' * len(self.street)
        masked_appNo = '*' * len(self.appNo)
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {masked_city}, Age: {self.age}, Pesel: {masked_pesel}, Street: {masked_street}, AppNo: {masked_appNo})"

with app.app_context():
    db.create_all()
