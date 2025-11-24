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
        no_mask = 0  # całe maskujemy
        masked_pesel = self.pesel[:no_mask] + '*' * (len(self.pesel) - no_mask)
        masked_street = self.street[:no_mask] + '*' * (len(self.street) - no_mask)
        masked_appNo = self.appNo[:no_mask] + '*' * (len(self.appNo) - no_mask)

        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age}, Pesel: {masked_pesel}, Street: {masked_street}, AppNo: {masked_appNo})"


with app.app_context():
    db.create_all()
