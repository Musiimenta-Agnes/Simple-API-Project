from app.extensions import db

class Sister(db.Model):
    __tablename__ = 'siters'


    id = db.Column(db.Integer, primary_key = True, nullable = False)
    first_name = db.Column(db.String(200), nullable = False)
    contact = db.Column(db.String(200), nullable = False, unique = True)
    email = db.Column(db.String(200), nullable = False, unique = True)
    password = db.Column(db.String(255), nullable = False, unique = True)
    address = db.Column(db.String(200), nullable = False)
    age = db.Column(db.Integer, nullable = True)
    image = db.Column(db.String(550), nullable = True)




    def __iit__(self, id, first_name, last_name, contact, email, password, address,image,age):
        self.id = id
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

