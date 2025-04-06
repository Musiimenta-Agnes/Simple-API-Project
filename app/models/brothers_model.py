from app.extensions import db

class Brother(db.Model):
    __tablename__ = "brothers"

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    first_name = db.Column(db.String(200), nullable = False)
    last_name = db.Column(db.String(200), nullable = False)
    contact = db.Column(db.String(200), nullable = False, unique = True)
    email = db.Column(db.String(200), nullable = False, unique = True)
    password = db.Column(db.String(255), nullable = False)
    address = db.Column(db.String(200), nullable = False)
    age = db.Column(db.Integer, nullable = True)
    image = db.Column(db.String(550), nullable = True)




    def __init__(self,first_name, last_name, contact, email, password, address,image,age):
        # We donot include the id because it is auto generated
        self.first_name= first_name
        self.last_name= last_name
        self.contact = contact
        self.email= email
        self.password= password
        self.address= address
        self.image= image
        self.age = age
        




    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

