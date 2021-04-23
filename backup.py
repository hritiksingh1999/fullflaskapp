from flask import Flask,request,Blueprint
from flask_restplus import Api , Resource , fields
from backend import db
from bson.json_util import dumps
import json
from waitress import serve

app = Flask(__name__)
api = Api(app)

signup_a= api.model('signup',{'user': fields.String('enter user name'),'email': fields.String('enter the email')})
post_a=api.model('post',{'user': fields.String('enter the user name'),'post': fields.String('enter the post')})
comment_a=api.model('postcomment',{'user': fields.String('enter the user who want to comment'), 'commented': fields.String("enter the name of the user you want to add comment"),'comment': fields.String("please enter the comment")})
forget_a= api.model('forgetid',{'user': fields.String('enter user name'),'email': fields.String('enter the email')})

username=db.username
posts=db.post
comment=db.comment

@api.route("/users")
class users(Resource):
    def get(self):
        a=db.username.find({},{'email': False,"_id": False,"password": False})
        return json.loads(dumps(a))


@api.route("/signup")
class signup(Resource):
    @api.expect(signup_a)
    def post(self):
        details=[]
        detail=api.payload
        details.append(dumps(detail))
        k=str(db.username.find().count()+1)
        username.insert({"_id":k})
        username.update({"_id":k}, detail)
        y=username.find({"_id":k},{"_id": True})
        return json.loads(dumps(y))

@api.route("/post/<id>")
class pos(Resource):
    @api.expect(post_a)
    def post(self,id):
        a=request.get_json()    
        b=json.loads(dumps(username.find({"_id":id})))
        m=b[0]['user']
        m1=a["user"]   
        if(m==m1):
            posts.insert(a)
            return "your post is live and its id is {} " .format(id)
        else:
            return "please enter correct id and password" 

@api.route("/getpost/<user>")
class getpost(Resource):
    def get(self,user):
        a1=[]
        print(dumps(posts.find()))
        a=json.loads(dumps(posts.find({"user":user},{"user":False})))
        for i in  range (0,len(a)):
            a1.append(a[i]["post"])
        return "user {} has posted {} " .format(user,a1)


@api.route("/getcomment/<user>")
class getcomment(Resource):
    def get(self,user):
        b=json.loads(dumps(posts.find({"user":user},{"_id":False,"user":False})))   
        a=json.loads(dumps(comment.find({"user":user},{"_id":False,"user": False})))
        return "user {} has posted {} and these are the comments {}" .format(user,b,a)

@api.route("/postcomment/<user>")
class postcomment(Resource):
    @api.expect(comment_a)
    def post(self,user):
        com=request.get_json()
        comment.insert(com)
        return "your comment is live on {}" .format(user)    


@api.route("/forgetid",methods=["POST"])
class forgetid(Resource):
    @api.expect(forget_a)
    def post(self):
        a=request.get_json()
        user=a["user"]
        email=a["email"]
        b=json.loads(dumps(username.find({"user":user,"email":email})))
        if (len(b)==0):
            return "please enter user name and emailId correctly"   
        else:
            id=b[0]['_id']
            return id

@api.route("/deleteuser/<user>",methods=["DELETE"])
class deleteuser(Resource):
    def delete(self,user):
        username.delete_one({"user":user})
        posts.delete_many({"user":user})
        comment.delete_many({"user":user})
        return "bye bye user {}" .format(user)

app.run(port=9000)