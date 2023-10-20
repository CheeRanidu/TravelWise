from flask import Flask, render_template, request, jsonify, make_response, url_for, redirect
from user import user_blueprint
import jwt
from functools import wraps
from config import secret_key
import json
app = Flask(__name__)




def require_token(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('jwtToken')

        if not token:
            return jsonify({'error': 'Token is missing unuathorized user'}), 401

        try:
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        

        return func(*args, **kwargs)

    return decorated_function


@app.route('/')
def home2():
    return render_template('index.html')


@app.route('/login')
def home():
    return render_template('login1.html')


@app.route('/signup')
def home1():
    return render_template('signup.html')


@app.route('/profile')
@require_token
def profile():
    return render_template('profile.html')


@app.route('/logout')
@require_token
def logout():
    response = make_response(redirect(url_for('home2')))
    response.set_cookie('jwtToken', '', expires=0, httponly=True, secure=True)
    
    return response

@app.route('/partner',methods=['POST', 'GET'])
@require_token
def partner():
     profile_json = request.args.get('profile',)
     profile = json.loads(profile_json)
     
     return render_template('partnerprofile.html', profile=profile)


app.register_blueprint(user_blueprint, url_prefix="/")


if __name__ == '__main__':
    app.run(debug=True)
