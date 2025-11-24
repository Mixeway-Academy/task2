from project import db, app

def mask_sensitive_data(data):
   # Zastępuje dane ciągiem gwiazdek o tej samej długości.
    if data is not None:
        return "*" * len(str(data))
    return "None"

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
        # print("Getting: " + str(self),flush=True)

    # def __repr__(self):
    #     return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age}, Pesel: {self.pesel}, Street: {self.street}, AppNo: {self.appNo})"
    def __repr__(self):
        return (
            f"Customer("
            f"ID: {self.id}, "
            f"Name: {mask_sensitive_data(self.name)}, "
            f"City: {mask_sensitive_data(self.city)}, "
            f"Age: {mask_sensitive_data(str(self.age))}, "
            f"Pesel: {mask_sensitive_data(self.pesel)}, "
            f"Street: {mask_sensitive_data(self.street)}, "
            f"AppNo: {mask_sensitive_data(self.appNo)}"
            f")"
        )

with app.app_context():
    db.create_all()
