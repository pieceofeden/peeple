from flask import Flask, request, jsonify, render_template,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import AddForm
import face_recognition
import subprocess
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'nosedive'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///'+os.path.join(APP_ROOT,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db =SQLAlchemy(app)
migrate = Migrate(app,db)

class user(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    facebook = db.Column(db.String)
    twitter = db.Column(db.String)
    linkedin = db.Column(db.String)
    github = db.Column(db.String)
    image = db.Column(db.String,nullable=False,default='')

    def __init__(self,name,email,facebook,twitter,linkedin,github,image):
        self.name = name
        self.email = email
        self.facebook = facebook
        self.twitter = twitter
        self.linkedin = linkedin
        self.github = github
        self.image = image

    def __repr__(self):
        return f"Name: {self.name},Email: {self.email}, facebook: {self.facebook}, twitter: {self.twitter}, linkedin: {self.linkedin}, github: {self.github} , Image: {self.image}"

class uploaded_images(db.Model):
    __tablename__ = 'uploaded_images'
    id = db.Column(db.Integer, primary_key = True)
    image = db.Column(db.String)

    def __init__(self,image):
        self.image = image

    def __repr__(self):
        return f'Uploaded_Image: {self.image}'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET','POST'])
def upload():
    target = os.path.join(APP_ROOT, 'uploaded_image/')
    print(target)

    if not os.path.isdir(target):
        os.makedirs(target)

    for file in request.files.getlist('file'):
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)

    image_info = uploaded_images(image = '')
    db.session.add(image_info)
    db.session.commit()
    path = os.path.join(APP_ROOT,'uploaded_image/')
    image_name = len(uploaded_images.query.all())
    for uploaded_image in os.listdir(path):
        count = 0
        for img in uploaded_images.query.all():
            if uploaded_image == img.image:
                break
            else:
                count+=1
        if(count == len(uploaded_images.query.all())):
            index = -1
            for letter in reversed(filename):
                if letter == '.':
                    break
                else:
                    index-=1
            ext = filename[index:]
            newname = str(image_name) + ext
            os.rename(path+uploaded_image,path+newname)
            img.image = newname
            break
        else:
            pass

    db.session.commit()
    return redirect(url_for('peep'))


# TODO: Complete this method
# Input: Uploaded image as request body parameter
# Output: List of people in the image
@app.route('/peep', methods=["GET"])
def peep():
    print('Peeping into people')

    string = ''
    os.chdir(APP_ROOT)
    uploaded_image_path = os.path.join(APP_ROOT,'uploaded_image/')
    known_image_path = os.path.join(APP_ROOT,'known_images/')

    os.chdir(uploaded_image_path)
    uploaded_image_id = len(os.listdir(uploaded_image_path))
    uploaded_image_info = uploaded_images.query.get(uploaded_image_id)
    uploaded_image = uploaded_image_info.image
    image = face_recognition.load_image_file(uploaded_image)
    face_locations = face_recognition.face_locations(image)
    face_encodings =  face_recognition.face_encodings(image)[0]

    os.chdir(known_image_path)
    unknown_encodings =  face_recognition.face_encodings(image)
    for unknown_encoding in unknown_encodings:
        known_count = 0
        unknown_count = 0
        for known_image in os.listdir(known_image_path):
            img = face_recognition.load_image_file(known_image)
            face_encodings = face_recognition.face_encodings(img)[0]
            result = face_recognition.compare_faces([face_encodings], unknown_encoding)
            if result == [True]:
                user_id =  known_image[:known_image.index('.')]
                known_count +=1
            else:
                unknown_count += 1
        if known_count != 0:
            user_info = user.query.get(int(user_id))
            user_name = user_info.name
            string += f' {user_name} '
        else:
            unknown_count = unknown_count/len(os.listdir(known_image_path))
            while(unknown_count != 0):
                string += ' Unknown '
                unknown_count -=1


    os.chdir(APP_ROOT)
    return f'<h1>{string}</h1>'

@app.route('/sign_up', methods=['GET','POST'])
def sign_up():
    form = AddForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        facebook = form.facebook.data
        twitter = form.twitter.data
        linkedin =  form.linkedin.data
        github = form.github.data
        new_user =  user(name,email,facebook,twitter,linkedin,github,image='')
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('sign_up_upload'))
    else:
        return render_template('sign_up.html',form=form)

@app.route('/sign_up_upload', methods=['POST','GET'])
def sign_up_upload():
    if request.method == "POST":
        target = os.path.join(APP_ROOT, 'known_images/')
        print(target)

        if not os.path.isdir(target):
            os.makedirs(target)

        for file in request.files.getlist('file'):
            print(file)
            filename = file.filename
            destination = "/".join([target, filename])
            print(destination)
            file.save(destination)
        for usr in user.query.all():
            if usr.image == '':
                user_id = usr.id
                path = os.getcwd()+'/known_images/'
                filename = os.listdir(path)[0]
                index = -1
                for letter in reversed(filename):
                    if letter == '.':
                        break
                    else:
                        index-=1
                ext = filename[index:]
                usr.image = str(user_id) + ext
                os.rename(path+filename,path+usr.image)

        db.session.commit()

        return redirect(url_for('user_list'))
    else:
        return render_template("sign_up_upload.html")

'''@app.route('/<user_id>')
def profile(user_id):
    user_info = user.query.get(int(user_id))
    user_name = user_info.name
    return f"{user_name}"'''

@app.route('/user_list')
def user_list():
    users = user.query.all()
    return render_template('user_list.html',users=users)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
