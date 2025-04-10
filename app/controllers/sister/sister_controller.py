from app.models.sister_model import Sister
from app.status_codes import HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_404_NOT_FOUND
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
            }),HTTP_500_INTERNAL_SERVER_ERROR
    



# Getting sister by id

@sister.get('/get/<int:id>/')
def get_sister_by_id(id):
    
    
    try:

        sister = Sister.query.filter_by(id=id).first()

        return jsonify({
            'message': 'Sister' +' ' + sister.get_full_name() + ' ' + 'has been successfully retrieved.',


            'sister': {
                'first_name':sister.first_name,
                'last_name':sister.last_name,
                'email':sister.email,
                'contact':sister.contact,
                'address':sister.address,
                'age':sister.age,
                'image':sister.image

            }
        })

    except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR
    



# Getting all sisters

@sister.route('/get', methods = ['GET'])
def get_all_sisters():
    try:

        all_sisters = Sister.query.all()
        sisters_data = []

        for sister in all_sisters:
            sister_info = {
                'first_name':sister.first_name,
                'last_name':sister.last_name,
                'email':sister.email,
                'contact':sister.contact,
                'address':sister.address,
                'age':sister.age,
                'image':sister.image
            }
            sisters_data.append(sister_info)

# Ensure this return is in the same line with for, or else you will get an error in postman of returning only one sister.
        return jsonify({
                'message': 'All sisters have been successifully retrieved',
                'total': len(sisters_data),
                'Sisters': sisters_data
            })
       




    except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR





# Deleting sister

@sister.route('/delete/<int:id>', methods = ['DELETE'])
def delete_sister(id):

    try:

        sister = Sister.query.filter_by(id = id).first()

        if not sister:
            return jsonify({'message': 'Sister with this id does not exist!'}),HTTP_404_NOT_FOUND
        else:
             db.session.delete(sister)
             db.session.commit()

             return jsonify({'message': 'Sister has ben successifully deleted'}),HTTP_500_INTERNAL_SERVER_ERROR
        
       

    except Exception as e:
        return jsonify({
            'error':str(e)
        },HTTP_500_INTERNAL_SERVER_ERROR)

