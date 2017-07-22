from flask import Flask, request, jsonify, make_response, abort,render_template

from data import User
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
# cors = CORS(app, resources={r"/*": {"origins": "http://localhost:63342\*"}})
app.secret_key = '123'
user = User()



@app.route('/', methods=['POST'])
def log():
    content = request.get_json(force=True)
    username = content["username"]
    password = content["password"]
    if username != "" and password != "":
        user_info = dict({"username": username, "password": password})
        result = user.user_login(user_info)
        return jsonify({"result": result})
    else:
        return jsonify(meg="请输入信息")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    content = request.get_json(force=True)
    username = content["username"]
    password = content["password"]
    info_user = dict({"username": username, "password": password})
    result = user.signup(info_user)
    return jsonify({"result": result})




@app.route('/write_post', methods=['POST'])
def write_posts():
    content = request.get_json(force=True)
    username =content["username"]
    post=content["post"]
    dicts = dict({"post": post, "username": username})
    user.post(dicts)
    return jsonify({"success":"success"})


@app.route('/comments', methods=["POST"])
def write_comments():
    content=request.get_json(force=True)
    dicts={
        "comment":content["comment"],
        "_id": content["_id"],
        "root_id": content["root_id"],
        # "order": request.json.get("order"),
        "username":content["username"]
    }
    result=user.comments(dicts)
    if result=="fail":
        return jsonify({"result": "fail"})
    else:
        return jsonify({"result":"success"})


@app.route('/community', methods=['POST'])
def read_posts():
    # username = request.json.get("username")
    content=request.get_json(force=True)
    order = content["order"]
    username=content["username"]
    result = user.read_post(dict({"order": order,"username":username}))
    return jsonify(result)

@app.route('/logout',methods=['POST'])
def logout():
    content=request.get_json(force=True)
    username = content['username']
    result = user.logout(username)
    return jsonify({"result":result})


@app.route('/praise', methods=['POST'])
def praise():
    content=request.get_json(force=True)
    _id = content["_id"]
    user.praise(_id)
    return jsonify({"success": "success"})


@app.route('/get_info', methods=["POST"])
def get_info():
    content=request.get_json(force=True)
    username = content["username"]
    dicts = dict({"username": username})
    data = user.get_info(dicts)
    if data == []:
        return jsonify(meg="无提醒")
    else:
        return jsonify(data)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run()
    app.debug = True
