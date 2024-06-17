import os
from flask import Flask , render_template, request, redirect, url_for, session
from deepface import DeepFace
import cv2


app = Flask("Analyze Face")
app.config["UPLOAD_FOLDER"] = './uploads'
app.config["ALLOWED_EXTENSIONS"] = {'png', 'jpg', 'jpeg'}

def auth(email, password):
    if email == "fahime@gmail.com" and password == "1234":
        return True
    else:
        return False
    

def allowed_file(filename):
    return True

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        my_email = request.form["email"]
        my_password = request.form["password"]
        result = auth(my_email, my_password)
        if result:
            # upload
            return redirect(url_for('upload'))

        else:
            # login
            return redirect(url_for('login'))
        
@app.route("/register")
def register():
    return render_template("register.html")
    
            

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == "GET":
        return render_template("upload.html")
    elif request.method == "POST":
        my_image = request.files['image']
        if my_image.filename == "":
            return redirect(url_for('upload'))
        else:
            if my_image and allowed_file(my_image.filename):
                save_path = os.path.join(app.config["UPLOAD_FOLDER"], my_image.filename)
                my_image.save(save_path)

                result = DeepFace.analyze(
                    img_path = save_path,
                    actions = ['age'],
                )

                age = result[0]['age']
                print(age)
                print(save_path)


                return render_template("result.html", age = age , uploaded_image =my_image.filename)
        
@app.route('/uploads/<filename>')
def send_uploaded_file(filename=''):
    from flask import send_from_directory
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/bmr", methods=['GET', 'POST'])
def bmr():
    if request.method == "GET":
        return render_template("bmr.html")
    elif request.method == "POST":
        my_weight = float(request.form["weight"])
        my_height = float(request.form["height"])
        my_age = int(request.form["age"])
        my_gender = request.form["gender"]
        
        if my_gender == "female":
            # woman bmr calculator
            bmr_result = (10 * my_weight) + (6.25 * my_height) - (5 * my_age) - 161
            

        elif my_gender == "male":
            # man bmr calculator
            bmr_result = (10 * my_weight) + (6.25 * my_height) - (5 * my_age) + 5
        else:
            # 
            print("Enter (female) or (male) for gender")
            return redirect(url_for('bmr'))
        
        return render_template("bmr.html", bmr_result=bmr_result)
       


# @app.route("/result")
# def result():
#     return render_template("result.html")

