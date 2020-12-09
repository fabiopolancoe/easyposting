from flask import Flask, redirect, url_for, request, render_template, abort, jsonify
import yaml

app = Flask(__name__)

def isdangerous(string):
    isdangerous = False
    blocked = ["<", ">", "ñ", "/", "!", '"', "'", "#", "$", "%", "&", "(", ")", "{", "}"]
    for blockedchar in blocked:
        for char in list(string):
            if char == blockedchar:
                isdangerous = True
            else:
                pass
    if isdangerous == True:
        abort(403)
    else:
        pass

@app.route('/post', methods = ['POST', 'GET'])
def post():
    with open('app/users.yaml', 'r') as users:
        user_data = yaml.load(users, Loader=yaml.FullLoader)

    if request.method == 'POST':
        isdangerous(request.form["username"])
        isdangerous(request.form["message"])

        if request.form["username"] in user_data:
            if user_data[request.form["username"]]["key"] == request.form["password"]:
                user_data[request.form["username"]]["post"] = request.form["message"]
                with open('app/users.yaml', 'w') as users:
                    users.write(yaml.dump(user_data))

                return render_template("output.html", title="Succesfully posted your announcement", text="We received the data of your post and successfully apdated your page.", redirect_url="/", redirect_text="Home")
            else:
                abort(401)
        else:
            abort(404)
    else:
        abort(404)

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    with open('app/users.yaml', 'r') as users:
        user_data = yaml.load(users, Loader=yaml.FullLoader)

    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']

        isdangerous(user)

        if user in user_data:
            return render_template("output.html", title="Failed to create account", text=f"The account '{user}' already exists, please choose another one.", redirect_url="/signup", redirect_text="Sign Up")
        else:
            user_data[user] = {'key': password, 'post': ''}
            with open('app/users.yaml', 'w') as users:
                users.write(yaml.dump(user_data))

            return render_template("output.html", title="Succesfully created your account", text=f"The account '{user}' has been succesfully created.", redirect_url="/", redirect_text="Home")
    else:
        return render_template("signup.html")

@app.route('/read')
def read():
    with open('app/users.yaml', 'r') as users:
        user_data = yaml.load(users, Loader=yaml.FullLoader)

    isdangerous(request.args.get("username"))

    if request.args.get("username") and request.args.get("username") in user_data:
        return jsonify(post=user_data[request.args.get("username")]["post"])
    else:
        abort(404)

@app.errorhandler(404)
def not_found(e):
    return render_template("output.html", title="404 Error", text="Sorry, this page does not exist (Or if you came from a form, the username you entered is not correct).", redirect_url="/", redirect_text="Home")

@app.errorhandler(401)
def unauthenticated(e):
    return render_template("output.html", title="401 Error", text="Sorry, the password you submitted is not correct.", redirect_url="/", redirect_text="Home")

@app.errorhandler(403)
def forbidden(e):
    return render_template("output.html", title="403 Error", text="You probably tried to use a special characters on an input. Special chars are <, >, ñ, /, !, \", \', #, $, %, &, (, ), { and }", redirect_url="/", redirect_text="Home")

@app.errorhandler(400)
def bad_request(e):
    return render_template("output.html", title="400 Error", text="Sorry, we could not handle that request.", redirect_url="/", redirect_text="Home")

@app.errorhandler(500)
def bad_request(e):
    return render_template("output.html", title="500 Error", text="Sorry, we have experienced an internal server error.", redirect_url="/", redirect_text="Home")

@app.route('/')
def root():
    return render_template("index.html")
