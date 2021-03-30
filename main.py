from flask import Flask,request,jsonify
import pymongo
from bson.objectid import ObjectId

connection_url = 'mongodb+srv://myUser:1234@cluster0.apvjp.mongodb.net/mydb?retryWrites=true&w=majority'
client = pymongo.MongoClient(connection_url)
app = Flask(__name__)

# Database
Database = client.get_database('mydb')
# Table
collection= Database.template
collection2= Database.register



@app.route("/Register",methods=["POST","GET"])
def reg():
    if request.method=='POST':
        data=request.get_json()
        data_insert={
            "f_name":data["first_name"],
            "l_name":data["last_name"],
            "email":data["email"],
            "password":data["password"]
        }
        collection.insert_one(data)
        return "Registered"

@app.route("/login",methods=["POST"])
def login():
    if request.method=='POST':
        data=request.get_json()
        data_insert={
            "email":data["email"],
            "password":data["password"]
        }
        result=collection.find_one(data_insert)
        if result:
            return "login"

        else:
            return "User not found"

@app.route("/template",methods=['POST','GET'])
def temp():
    if request.method=='POST':
        data=request.get_json()
        data_insert={
                'template_name': data['template_name'],
                'subject':data['subject'],
                'body':data['body'],
        }
        collection2.insert_one(data_insert)
        return "Template is created"

    if request.method=='GET':
        tmp=collection2.find_one()
        data_to_display= {
            'subject': tmp['subject'],
            'body': tmp['body'],
            'template_name': tmp['template_name'],
        }
        return data_to_display

@app.route("/template/<Id>",methods=["DELETE",'PUT'])
def temp_delete(Id):
    if request.method=='DELETE':
        collection2.delete_one({"_id":ObjectId(Id)})
        return "Deleted"
    if request.method == 'PUT':
        #old_data=collection2.find_one({"_id":ObjectId(Id)})
        new_data=request.get_json()
        # old_data['subject']=new_data['subject']
        # old_data['body']=new_data['body']
        # old_data['template_name']=new_data['template_name']

        collection2.update_one({"_id":ObjectId(Id)},{'$set':{'subject':new_data['subject'],'body':new_data['body'],'template_name':new_data['template_name']}})
        return "Updated"




if __name__=="__main__":
    app.run(debug=True)