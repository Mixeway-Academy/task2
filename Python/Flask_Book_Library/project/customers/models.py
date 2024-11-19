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
        #masked_name = Customer.data_masker(self.name)
        masked_city = Customer.data_masker(self.city)
        #masked_age = Customer.data_masker(self.age)
        masked_pesel = Customer.data_masker(self.pesel)
        masked_street = Customer.data_masker(self.street)
        masked_appNo = Customer.data_masker(self.appNo)
        #return f"Customer(ID: {self.id}, Name: {masked_name}, City: {masked_city}, Age: {masked_age}, Pesel: {masked_pesel}, Street: {masked_street}, AppNo: {masked_appNo})"
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {masked_city}, Age: {self.age}, Pesel: {masked_pesel}, Street: {masked_street}, AppNo: {masked_appNo})"

    @staticmethod
    def data_masker(data_to_be_masked):
        mask_len = len(data_to_be_masked)
        if mask_len == 0:
            mask = '***********'
        else:
            mask = '*'*mask_len
        return mask


with app.app_context():
    db.create_all()
