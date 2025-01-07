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
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {mask_data(self.city, 1)}, Age: {self.age}, Pesel: {mask_data(self.pesel)}, Street: {mask_data(self.street, 1)}, AppNo: {mask_data(self.appNo)})"

def mask_data(data, visible_start=0, mask_char="*"):
    if isinstance(data, int):
        return (mask_char * 3)
    elif isinstance(data, str):
        masked_length = max(0, len(data) - visible_start)
        return data[:visible_start] + (mask_char * masked_length)
    return "N/A"

with app.app_context():
    db.create_all()
