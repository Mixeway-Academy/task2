from project.core.special_objects import ReadOnce
from project import db, app


# Customer model
class CustomerDBModel(db.Model):
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



with app.app_context():
    db.create_all()


class Customer:
    def __init__(self, name, city, age, pesel, street, appNo):
        self.db_model = CustomerDBModel(name, city, age, pesel, street, appNo)
        self.name = name
        self.city = city
        self.age = age
        self.pesel = ReadOnce(pesel)
        self.street = ReadOnce(street)
        self.appNo = ReadOnce(appNo)
        print("Getting: " + str(self),flush=True)

    @classmethod
    def from_db(cls, customer_model):
        return cls(
            name=customer_model.name,
            city=customer_model.city,
            age=customer_model.age,
            pesel=customer_model.pesel,
            street=customer_model.street,
            appNo=customer_model.appNo
        )
    def set_name(self, name):
        self.name = name
        self.db_model.name = name
    def set_city(self, city):
        self.city = city
        self.db_model.city = city
    def set_age(self, age):
        self.age = age
        self.db_model.age = age

    @staticmethod
    def get(id):
        customer_model = CustomerDBModel.query.get(id)
        if customer_model:
            return Customer.from_db(customer_model)
        return None
    def __repr__(self):
        return f"Customer(Name: {self.name}, City: {self.city}, Age: {self.age}, Pesel: {self.pesel}, Street: {self.street}, AppNo: {self.appNo})"