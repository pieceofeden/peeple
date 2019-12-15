from flask import Flask, request, jsonify, render_template
import os
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

#Homepage of the webapp
@app.route('/')
def index():
    return render_template('index.html')

#upload part 
@app.route('/upload', methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    print(target)

    if not os.path.isdir(target):
        os.makedirs(target)

    for file in request.files.getlist('file'):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)

    return render_template('upload_completed.html')


# TODO: Complete this method
# Input: Uploaded image as request body parameter
# Output: List of people in the image
@app.route('/peep', methods=["GET"])
def peep():
    print('Peeping into people')
    return (jsonify(
        {
            'code': 200,
            'people': [
                {
                    'name': 'Name',
                    'email': 'Email',
                    'links': {
                        'facebook': '',
                        'twitter': '',
                        'linkedin': '',
                        'github': ''
                    }
                }
            ]
        }
    ))

# TODO: Complete this method
# Input: Person details as request body parameter
# Output: 200 code if validations pass, else error message
@app.route('/users', methods=["POST"])
def register_user():
    # Use the request.args
    print('Register a new user')
    return(jsonify({'code': 200, 'id': 1}))

# TODO: Complete this method
# Input: Person details as request body parameter
# Output: True if validations pass, else error message
@app.route('/users/<int:user_id>', methods=["POST"])
def update_user(user_id):
    # Fetch user from database for this user_id
    # Use the request.args
    print('Updates an existing user')
    return(jsonify({'code': 200}))

# TODO: Complete this method
# Input: Person details as request body parameter
# Output: True if validations pass, else error message
@app.route('/users/<int:user_id>', methods=["GET"])
def fetch_user(user_id):
    # Fetch user from database for this user_id
    print('Fetches an existing user')
    return (jsonify(
        {
            'code': 200,
            'person': {
                'name': 'Name',
                'email': 'Email',
                'links': {
                    'facebook': '',
                    'twitter': '',
                    'linkedin': '',
                    'github': ''
                }
            }
        }
    ))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
