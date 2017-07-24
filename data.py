from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from werkzeug.security import check_password_hash, generate_password_hash

client = MongoClient('localhost', 27017)
print(client.address)
print(client.HOST)
db = client['user']
# 数据库结构 采用内嵌（采用分布式）
post_coll = db["post_info"]
user_coll = db["user_info"]
post_info = {
    "content": "",
    "post_time": datetime.now(),
    "praise_count": 0,
    "username": "",
    "comment_by": [],
    "read": [],
    "order": 0,
    "tag": [],
    "comment_who": ObjectId(),
    "root_id": ObjectId()
}
user_info = {
    "username": "",
    "password": "",
    "state": False,
    "items": []
}


class User():
    """

    """
    def __init__(self):
        pass

    def signup(self, dicts):
        if user_coll.find({"username": dicts["username"]}).count() >= 1:
            return False
        security_password = generate_password_hash(dicts["password"])
        user_coll.insert({"username": dicts["username"], "password": security_password, "state": False,"items":[]})
        return True

    def activite(self, username):
        user_coll.update({"username": username}, {"$set": {"state": True}})

    def check_activity(self, username):
        if user_coll.find({"username": username, "state": True}).count() == 1:
            return True
        else:
            return False

    def logout(self, username):
        user_coll.update({"username": username}, {"$set": {"state": False}})
        if self.check_activity(username) is True:
            return False
        return True

    def user_login(self, dicts):
        security_password = user_coll.find_one({"username": dicts["username"]}, {"password": 1, "_id": 0})
        if security_password and check_password_hash(security_password["password"], dicts["password"]):
            self.activite(dicts["username"])
            return True
        else:
            return False

    def post(self, dicts):
        if self.check_activity(dicts["username"]) is True:
            max_cursor = post_coll.find().sort("order", -1).limit(1)
            max_order = 0
            for post in max_cursor:
                max_order = post["order"]
                break
            post_id = post_coll.insert(
                {"content": dicts["post"], "post_time": datetime.now(), "order": max_order + 1, "praise_count": 0,
                 "username": dicts["username"], "comment_by": [],"read":[],"tag":[]})
            user_coll.update({"username": dicts["username"]}, {"$push": {"items": ObjectId(post_id)}})
            return True
        else:
            return False

    def get_info(self, dicts):
        data = []
        if self.check_activity(dicts["username"]):
            for cursor in post_coll.find({"username": dicts["username"]}):
                temp_id = cursor["_id"]
                length = len(cursor["comment_by"])
                for loop in range(length):
                    if cursor["read"][loop] is False:
                        post_coll.update({"_id": temp_id}, {"$set": {"read"[loop]: True}})
                        # cursor["read"][loop] = True
                        content = post_coll.find_one({"_id": temp_id}, {"content": 1, "_id": 0})
                        # post_coll.update({cursor["comment_by"][loop]:_id}, {"$set": {"comment_by"[loop]: True}})
                        data.append(dict({loop: content["content"]}))
        return data

    def comments(self, dicts):
        if self.check_activity(dicts["username"]) is True:
            post_id = post_coll.insert(
                {"content": dicts["comment"], "post_time": datetime.now(), "comment_who": ObjectId(dicts["_id"]),
                 "praise_count": 0, "order": 0,"comment_by":[],"read":[],
                 "username": dicts["username"], "root_id": ObjectId(dicts["root_id"])})
            user_coll.update({"username": dicts["username"]}, {"$push": {"items": ObjectId(post_id)}})
            if dicts["_id"] == dicts["root_id"]:
                post_coll.update({"_id": ObjectId(dicts["_id"])},
                                 {"$push": {"comment_by": ObjectId(post_id), "read": False}})
            else:
                post_coll.update({"_id": ObjectId(dicts["_id"])},
                                 {"$push": {"comment_by": ObjectId(post_id), "read": False}})
                post_coll.update({"_id": ObjectId(dicts["root_id"])},
                                 {"$push": {"comment_by": ObjectId(post_id), "read": False}})
            return "success"
        return "fail"

    def praise(self, _id):
        post_coll.update({"_id": ObjectId(_id)}, {"$inc": {"praise_count": 1}})
        return True

    def read_post(self, dicts):
        """
        若是第一次读取数据选择post最大的内容返回，此后依次选择order小的返回
        :param dicts:
        :return:
        """
        if self.check_activity(dicts["username"]) is False:
            return -1
        result = []
        order = dicts["order"]
        temp_order = 0
        if order==-1:
            temp_dict={"content":"到底了"}
            result.append(temp_dict)
            result.append(order)
            return result
        elif order == 0:
            cursor = post_coll.find().sort("order", -1).limit(1)
            for posts in cursor:
                temp_dict = {
                    "content": posts["content"],
                    "post_time": posts["post_time"],
                    "praise_count": posts["praise_count"],
                    "username": posts["username"],
                    "_id": str(posts["_id"])
                }
                temp_order = posts["order"]
                result.append(temp_dict)
                for loop in posts["comment_by"]:
                    temp = post_coll.find_one({"_id": loop})
                    temp_dict = {
                        "content": temp["content"],
                        "post_time": temp["post_time"],
                        "praise_count": temp["praise_count"],
                        "username": temp["username"],
                        "_id": str(temp["_id"]),
                        "root_id": str(temp["root_id"])
                    }
                    result.append(temp_dict)

                break
            result.append(temp_order)
            return result
        else:
            posts = post_coll.find_one({"order": order})
            temp_dict = {
                "content": posts["content"],
                "post_time": posts["post_time"],
                "praise_count": posts["praise_count"],
                "username": posts["username"],
                "_id": str(posts["_id"])
            }
            result.append(temp_dict)
            for loop in posts["comment_by"]:
                temp = post_coll.find_one({"_id": loop})
                temp_dict = {
                    "content": temp["content"],
                    "post_time": temp["post_time"],
                    "praise_count": temp["praise_count"],
                    "username": temp["username"],
                    "_id": str(temp["_id"]),
                    "root_id": str(temp["root_id"])
                }
                result.append(temp_dict)
            result.append(order)
            return result

    def recommend(self):
        pass
# def to_json(self):
#     return {
#         'id': str(self.id),
#         'content': self.content,
#         'time': self.time,
#         'state': self.status
#     }
