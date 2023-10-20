from flask import Blueprint, request, jsonify
import bcrypt
from config import client, db, collection, collection1
import jwt
import datetime
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import secret_key


user_blueprint = Blueprint("user", __name__)




@user_blueprint.route('/login', methods=['POST'])
def login():
        # Get the request data
    request_data = request.get_json()

    # Extract username and password from the request data
    email = request_data.get('email')
    password = request_data.get('password')

    # Check if the username and password are provided
    if not email or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Retrieve the user from the database by email
    user = collection.find_one({'email': email})

    # Check if the user exists and the password is correct using bcrypt
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        # Create a payload for the JWT
        payload = {
            'user_id': str(user['_id']),  # Convert ObjectId to string
            'email': user['email'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Expiration time
        }

        # Create the JWT
        token = jwt.encode(payload, secret_key, algorithm='HS256')

        # Return the JWT to the client
        response = jsonify({'message': 'Login successful'})
        response.set_cookie('jwtToken', token, httponly=True, secure=True)
        return response
 
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


@user_blueprint.route('/signup', methods=['POST'])
def signup():
    # Get the request data
    request_data = request.get_json()

    # Extract email, name, and password from the request data
    email = request_data.get('email')
    password = request_data.get('password')
    firstName = request_data.get('firstName')
    lastName = request_data.get('lastName')
    gender = request_data.get('gender')
    number = request_data.get('number')

    # Check if the email, name, and password are provided
    if not email or not firstName or not password:
        return jsonify({'error': 'Email, name, and password are required'}), 400

    # Check if the email already exists in the database
    existing_user = collection.find_one({'email': email})
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 400

    # Hash the provided password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Store the email, name, and hashed password in the database
    user_data = {
        'email': email,
        'password': hashed_password.decode('utf-8'),  # Store as string
        'firstName':firstName,
        'lastName':lastName,
        'gender':gender,
        'number':number
    }
    collection.insert_one(user_data)

    response =  jsonify({'message': 'Registration successful'}), 201
    return response


@user_blueprint.route('/partner', methods=['POST'])
def partner():
    # Get the request data
    request_data = request.get_json()

    # Extract email, name, and password from the request data
    name = request_data.get('name')
    age = request_data.get('age')
    marital = request_data.get('marital')
    interest = request_data.get('interest')
    aboutme = request_data.get('aboutme')
    nationalid = request_data.get('nationalid')
    email = request_data.get('email')

    # Check if the email already exists in the database
    existing_user = collection1.find_one({'nationalid': nationalid})
    if existing_user:
        return jsonify({'error': 'user already registered'}), 400

    # Store the email, name, and hashed password in the database
    user_data = {
        'age': age,
        'name': name,
        'email': email,
        'marital': marital,
        'interest': interest,
        'nationalid': nationalid,
        'aboutme': aboutme,
    }
    collection1.insert_one(user_data)

    return jsonify({'message': 'Registration successful'}), 201


@user_blueprint.route('/predict', methods=['POST', 'GET'])
def predict():
    request_data = request.get_json()

    age = request_data.get('age')
    ms = request_data.get('ms')
    trvl = request_data.get('trvl')
    myself = request_data.get('myself')

    data_dict = {
        'Age': age,
        'MaritalStatus': ms,
        'Travel': trvl,
        'Myself': myself
    }

    # Create a Pandas DataFrame from the data dictionary
    df1 = pd.DataFrame([data_dict])

    #  Query MongoDB to retrieve data
    data_from_mongodb = list(collection1.find({}, {"_id": 0}))

    df = pd.DataFrame(data_from_mongodb)

    print(df)
    print(df1)

    # Preprocess the travel partner data and extract descriptions
    df['combined_description'] = df['aboutme'].fillna('') + ' ' + df['age'].astype(str).fillna('') + ' ' + df['interest'].fillna('') + ' ' + df['marital'].fillna('')
    df1['combined_description'] = df1['Myself'].fillna('') + ' ' + df1['Age'].astype(str).fillna('') + ' ' + df1['Travel'].fillna('') + ' ' + df1['MaritalStatus'].fillna('')


    travel_partner_descriptions = df['combined_description'].tolist()
    traveler_descriptions = df1['combined_description'].tolist()

    

    # Create a TF-IDF vectorizer and fit it on the travel partner descriptions
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(travel_partner_descriptions)
    tfidf_vector = tfidf_vectorizer.transform(traveler_descriptions)

    print(tfidf_matrix)
    print("asdad")
    print(tfidf_vector)

    # Compute cosine similarity between the user and travel partners
    cosine_sim = cosine_similarity(tfidf_vector, tfidf_matrix)

    # Get the indices of top recommendations based on similarity scores
    top_recommendations = cosine_sim[0].argsort()[::-1][:5]

    # top_recommendations = cosine_sim.argsort()[0][::-1]

    print(cosine_sim)
    print(top_recommendations)

    recommended_profiles = []

    for index in top_recommendations:
        profile = {
            'name': df['name'][index],
            'age': df['age'][index],
            'aboutme': df['aboutme'][index],
            'email': df['email'][index],
            'similarity_score': cosine_sim[0][index]
        }
        recommended_profiles.append(profile)

    # Return the recommended profiles as part of the JSON response
    return jsonify({'profiles': recommended_profiles}), 201



    
