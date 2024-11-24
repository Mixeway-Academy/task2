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
        self.name2 = self.name.split()
        self.firstname = self.name2[0]
        self.surname = self.name2[1]

        return f"Customer(ID: {self.id}, Name: {self.firstname + ' ' + self.surname[0] + ('*' * (len(self.surname)-1))}, City: {self.city[0]+('*' * (len(self.city)-1))}, Age: {'*' * len(self.age)}, Pesel: {'*' * len(self.pesel)}, Street: {self.street[0]+('*' * (len(self.street)-1))}, AppNo: {'*' * len(self.appNo)})"


with app.app_context():
    db.create_all()
