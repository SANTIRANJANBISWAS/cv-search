from flask import Flask 
from flask import render_template
from flask import request
from flask import session
from flask.wrappers import Request


from flask_pymongo import PyMongo

app = Flask(__name__) 
app.secret_key = "santi" #For Create Session 


mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/finalproject")
db = mongodb_client.db
 
@app.route('/')  
def indexpage():  
    return render_template('index.html')

@app.route('/studentregistration', methods=["GET", "POST"])  
def studentregistrationpage():
    if request.method == 'GET':
        return render_template('studentregistration.html')
    else:
        uname = request.form['Username']
       
        db.santi.insert_one(
        {'username': uname,
        'useruniversityrollno':request.form['universityrollno'],
        'userdept':request.form['DEPT'],
        'usersession':request.form['SESSION'],
        'userprofilegithublink':request.form['profilegithub_link'],
        'useremail': request.form['Email_Id'],
        'usercity':request.form['City'],
        'userpincode':request.form['Pin_Code'],
        'usermobile': request.form['Mobile_Number'],
        'usercountry': request.form['Country'],
        'usergender': request.form['Gender'],
        'userdob': request.form['Birthday_day'],
        'userpass': request.form['password'],
        'useraddress': request.form['Address'],
        
        })
       
        return render_template('studentregistration.html',msg = "REGISTRATION SUCCESSFUL")
        


@app.route('/studentlogin', methods=["GET", "POST"])  
def studentloginpage(): 
    if request.method == 'GET': 
        return render_template('studentlogin.html')
    else:
        user = db.santi.find_one(
        {'useremail': request.form['Email_Id'],
         'userpass': request.form['password'],
        })
        print(user)
        
        if user:
            #print(user['username'])
            session['Email_Id']= user['useremail']
            session['password'] = user['userpass']
            session['usertype']= 'USER'
            return render_template('studentafterlogin.html', uname = user['username'])
        else:
            return render_template('studentlogin.html', errormsg = "INVALID UID OR PASSWORD")

@app.route('/studentafterlogin', methods=["GET", "POST"])  
def studentafterloginpage(): 
    if request.method == 'GET': 
        return render_template('studentafterlogin.html')


@app.route('/contactus', methods=["GET", "POST"])  
def contactpage():
    if request.method == 'GET':
        return render_template('contactus.html')
    else:
        db.contactus.insert_one({
        'userfirstname': request.form['firstname'],
         'userlastname': request.form['lastname'],
         'usersubject': request.form['subject'],
        'usercountry': request.form['country'],
    
        })
        return render_template('contactus.html',msg = " SUCCESSFUL")
@app.route('/about', methods=["GET", "POST"])  
def aboutpage():
    if request.method == 'GET':
        return render_template('about.html')

@app.route('/cdclogin', methods=['GET','POST'])  
def cdcloginpage(): 
    if request.method == 'GET':
        return render_template('cdclogin.html')
    else:      
        useruid = request.form['Username']
        userpass = request.form['password']

        if(useruid == 'admin' and userpass == 'admin'):
            return render_template('cdcafterlogin.html')
        else:
            return render_template('cdclogin.html', msg = 'INVALID UID OR PASS')

@app.route('/cdchome')  
def cdcafterlogin(): 
    return render_template('cdcafterlogin.html')

@app.route('/viewall')  
def viewall(): 
    userobj = db.santi.find({})
    print(userobj)
    return render_template('viewall.html', userdata = userobj)


@app.route('/search', methods=['GET','POST'])  
def search1(): 
    if request.method == 'GET':
        return render_template('search.html')
    else:      
        userobj = db.santi.find_one(
        {'useremail': request.form['Email_Id']})
        print(userobj)
        
        if userobj:
            #print(userobj['username'])
            return render_template('search.html', userdata = userobj,show_results=1)
        else:
            return render_template('search.html', errormsg = "INVALID EMAIL ID")


@app.route('/search by roll', methods=['GET','POST'])  
def search2(): 
    if request.method == 'GET':
        return render_template('search by roll.html')
    else:      
        userobj = db.santi.find_one(
        {'useruniversityrollno': request.form['universityrollno']})
        print(userobj)
        
        if userobj:
            #print(userobj['username'])
            return render_template('search by roll.html', userdata = userobj,show_results=1)
        else:
            return render_template('search by roll.html', errormsg = "INVALID  Roll No")

            

@app.route('/search by session&dept', methods=['GET','POST'])  
def search3(): 
    if request.method == 'GET':
        return render_template('search by session&dept.html')
    else:      
        userobj = db.santi.find_one(
        {'usersession': request.form['SESSION'],
        'userdept': request.form['DEPT']})
        print(userobj)
        
        if userobj:
            #print(userobj['username'])
            return render_template('search by session&dept.html', userdata = userobj,show_results=1)
        else:
            return render_template('search by session&dept.html', errormsg = "INVALID SESSION AND DEPT")

@app.route('/search view contacts', methods=['GET','POST'])  
def search4():
    if request.method == 'GET':
        return render_template('search view contacts.html')
    else:      
        userobj = db.santi.find_one(
        {'usermobile': request.form['Mobile_Number'],})
        print(userobj)
        
        if userobj:
            #print(userobj['username'])
            return render_template('search view contacts.html', userdata = userobj,show_results=1)
        else:
            return render_template('search view contacts.html', errormsg = "INVALID CONTACT NO")

@app.route('/delete', methods=['GET','POST'])  
def delete(): 
    if request.method == 'GET':
        return render_template('delete.html')
    else:      
        responsefrommongodb = db.santi.find_one_and_delete(
        {'useremail': request.form['email']})
        print(responsefrommongodb)
        if responsefrommongodb is not None:
            return render_template('delete.html', msg = "SUCCESSFULLY DETELED")
        return render_template('delete.html', msg = "INVALID EMAIL ID")

@app.route('/delete', methods=['POST'])  
def deleteUser1():
    print(request.form['email']) 
    responsefrommongodb = db.santi.find_one_and_delete({'useremail': request.form['email']})
    print(responsefrommongodb)
    return redirect(url_for('viewall'))


@app.route('/viewprofile')  
def viewProfile(): 
    uemail = session['Email_Id']      
    userobj = db.santi.find_one({'useremail': uemail})
    print(userobj)
    return render_template('viewprofile.html', userdata = userobj)
    
@app.route('/updateprofile', methods=["GET", "POST"])  
def updateProfile():
    if request.method == 'GET':
        uemail = session['Email_Id']      
        userobj = db.santi.find_one({'useremail': uemail})
        return render_template('updateprofile.html',userdata = userobj)
    else:
        db.santi.update_one( {'useremail': session['Email_Id'] },
        { "$set": { 'usermobile': request.form['Mobile_Number'],
                    'userpass': request.form['password'],
                    'useraddress': request.form['Address'] 
                  } 
        })
        return redirect(url_for('viewProfile'))


if __name__ == '__main__':  
   app.run(debug = True)  