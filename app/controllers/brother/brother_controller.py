from flask import Blueprint, request,jsonify
from app.models.brothers_model import Brother
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_200_OK
import validators
from app.extensions import db,bcrypt
from flask_jwt_extended import jwt_required


# Define the route

bro = Blueprint('bro',__name__,url_prefix='/api/v1/bro')

@bro.route('/register', methods = ['POST'])
def register_brother():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact = data.get('contact')
    email = data.get('email')
    password= data.get('password')
    address = data.get('address')
    age = data.get('age')
    image = data.get('image')

    # Validation of data and data redundance
    if not first_name or not last_name or not email or not password or not contact or not address:
        return jsonify({'error': 'All fields are required!'}),HTTP_400_BAD_REQUEST
    
    # validation of the email
    if not validators.email (email):
        return jsonify({'error':'invalid email'}),HTTP_400_BAD_REQUEST
    
    #Length of the password
    if len(password) < 8:
        return jsonify({'error':'Password is short!'}),HTTP_400_BAD_REQUEST
    
    # Filterng through the model to check whether the email or contact already exists.

    if Brother.query.filter_by(email=email).first() is not None:
        return jsonify({'error':'Email already in use!'}),HTTP_409_CONFLICT
    
    if Brother.query.filter_by(contact=contact).first() is not None:
        return jsonify({'error':'Contact already in use!'}),HTTP_409_CONFLICT
    
    # Try securing the password by hashing it
    try:

        hashed_password = bcrypt.generate_password_hash(password)

        # Create a new instance for the brother and ensure to include everything that you mentioned in your model.

        new_data = Brother(first_name=first_name,last_name=last_name,email=email,contact=contact,password=hashed_password,address=address,age=age,image=image)

        # dd and commit this information into the database
        db.session.add(new_data)
        db.session.commit()
       


        # Create function to keep track of brother's  full name

        full_name = new_data.get_full_name()

        # Return the brother's full name as succefully created
        return jsonify({
            'message': full_name + "has been successfully registered as a new brother",
            'brother': {
                
                'first_name':new_data.first_name,
                'last_name':new_data.last_name,
                'email':new_data.email,
                'contact':new_data.contact,
                'address':new_data.address,
                'age':new_data.age,
                'image':new_data.image

                
            }

        }),HTTP_201_CREATED



    except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR



#Get brother by id

@bro.get('/brother/<int:id>')
def get_bro_by_id(id):

    try:

        brother = Brother.query.filter_by(id=id).first()

        return jsonify({
            'message':'Brother' +' ' + brother.get_full_name() + ' ' + 'has been successfully retrieved.',


            'brother': {
                'id':brother.id,
                'first_name':brother.first_name,
                'last_name':brother.last_name,
                'email':brother.email,
                'full_name':brother.get_full_name(),
                'contact':brother.contact,
                'address':brother.address,
                'age':brother.age,
                'image':brother.image

            }
        })




    except Exception as e:
        return jsonify({
            'error': str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR

    
