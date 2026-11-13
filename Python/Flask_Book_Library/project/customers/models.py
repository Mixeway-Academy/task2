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
        masked = self.get_masked_data()
        return (f"Customer(ID: {self.id}, Name: {self.name}, "
                f"City: {masked['city']}, Age: {self.age}, "
                f"Pesel: {masked['pesel']}, Street: {masked['street']}, "
                f"AppNo: {self.appNo})")
    def get_masked_data(self):
        return {
            'pesel': '*' * len(self.pesel) if self.pesel else "None",
            'street': '*' * len(self.street) if self.street else "None",
            'city': '*' * len(self.city) if self.city else "None"
        }


with app.app_context():
    db.create_all()
