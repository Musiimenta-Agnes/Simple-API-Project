from app.models.sister_model import Sister
from app.status_codes import HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT
from flask import Blueprint,request,jsonify
import validators
from flask_jwt_extended import jwt_required
from app.extensions import bcrypt,db

#register blue prints

sister = Blueprint('sis',__name__,url_prefix='/api/v1/sis')

#Decorator
@sister.route('/register',methods = ['POST'])
def register_sister():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact = data.get('contact')
    email = data.get('email')
    password= data.get('password')
    address = data.get('address')
    age = data.get('age')
    image = data.get('image')

    #Validating the credentials

    if not first_name or not last_name or not contact or not email or not password or not address:
        return jsonify({'error':'All fields are required!'}),HTTP_400_BAD_REQUEST
    
    if len(password) < 5:
        return jsonify({'error':'Password is too short!'}),HTTP_400_BAD_REQUEST
    
    if not validators.email(email):
        return jsonify({'error':'Invalid email!'}),HTTP_400_BAD_REQUEST
    
    # Make queries for more auhtentication

    if Sister.query.filter_by(email=email).first() is not None:
        return jsonify({'error':'Email already in use!'}),HTTP_409_CONFLICT
    
    if Sister.query.filter_by(contact=contact).first() is not None:
        return jsonify({'error':'Email already in use!'}),HTTP_409_CONFLICT
    

    # Try hashing the password for more security
    try:

        hashed_password = bcrypt.generate_password_hash(password)

        new_data = Sister(first_name=first_name,last_name=last_name,contact=contact,email=email,
                          password=hashed_password,address=address,age=age,image=image)
        
        # Register the new data
        db.session.add(new_data)
        db.session.commit()

# Generating the full name
        full_name = new_data.get_full_name()


#New data to be returned after registration
        return jsonify({
              'message': full_name + "has been successfully registered as a new sister",
            'sister': {
                
                'first_name':new_data.first_name,
                'last_name':new_data.last_name,
                'email':new_data.email,
                'contact':new_data.contact,
                'address':new_data.address,
                'age':new_data.age,
                'image':new_data.image
            }

           }),HTTP_200_OK
           
        



    except Exception as e:
        return jsonify({
            'error': str(e)
            })
    

