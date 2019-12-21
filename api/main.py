from flask import Flask, request, jsonify, render_template
import subprocess
import os
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

#Homepage of the webapp
#Creates a folder known_people
@app.route('/')
def index():
    return render_template('index.html')

#Upload Part
#Uploaded Images are saved in the images folder
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

    count = 1
    path = os.getcwd()+'/images/'
    for filename in os.listdir(path):
        ext = filename[filename.index('.'):]
        newname = str(count)+ ext
        os.rename(path+filename,path+newname)
        count+=1


    return render_template('upload_completed.html')


# TODO: Complete this method
# Input: Uploaded image as request body parameter
# Output: List of people in the image
@app.route('/peep', methods=["GET"])
def peep():
    subprocess.call(['face_recognition', './known_people/', './images/'],stdout=open('Output.txt', 'wb'))
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

@app.route('/register')
def register():
    print('Register a new user')
    return render_template('register.html')

# TODO: Complete this method
# Input: Person details as request body parameter
# Output: 200 code if validations pass, else error message
@app.route('/users', methods=['POST'])
def users():
    target = os.path.join(APP_ROOT, 'known_people/')
    print(target)

    if not os.path.isdir(target):
        os.makedirs(target)

    for file in request.files.getlist('file'):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)

    lst = []
    count = 1
    path = os.getcwd()+'/known_people/'
    for filename in os.listdir(path):
        person_name = filename[:filename.index('.')]
        ext = filename[filename.index('.'):]
        try:
            type(int(person_name))==str
        except ValueError:
            newname = str(count) + ext
            os.rename(path+filename,path+newname)
            lst.append({"name": person_name, "id": count})
        else:
            newname = str(count) + ext
            os.rename(path+filename,path+newname)
        count+=1

    json_dict = { "people" : lst }

#Code to be added to send the user's data to a database

    return jsonify(json_dict, 200)

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
