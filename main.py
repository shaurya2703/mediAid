from flask import Flask,render_template , request , jsonify , redirect , url_for , make_response
from flask_sqlalchemy import SQLAlchemy 
import razorpay
import numpy as np
import pickle
import math


app = Flask(__name__)
model = pickle.load(open('diabetesmodel.pkl','rb'))
model1 = pickle.load(open('heartmodel.pkl','rb'))
model2 = pickle.load(open('cancermodel.pkl','rb'))

app.config['SECRET_KEY'] = 'PAYMENT_APP'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payments.db'
db  = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    email = db.Column(db.String(120),nullable=False)
    name = db.Column(db.String(120),nullable=False)
    purpose = db.Column(db.String(200),nullable=False)
    amount = db.Column(db.String(120),nullable=False)

    def __repr__(self):
        return f"User('{self.name}' , '{self.email}' , '{self.purpose}' , '{self.amount}' )"

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/index')
def patient_page():
    return render_template('index.html')

@app.route('/doctor')
def doctor_page():
    return render_template('doctor_landing.html', users = User.query.all())

@app.route('/patient_detail')
def patient_detail():
    user_name = request.form.get('user_name')
    user_disease = request.form.get('user_disease')
    return render_template('patient_detail.html', name=user_name , disease = user_disease)

@app.route("/heart")
def heart():
    return render_template('heart.html')

@app.route("/diabetes")
def diabetes():
    return render_template('diabetes.html')

@app.route("/cancer")
def cancer():
    return render_template('cancer.html')

@app.route("/health_checkup_online")
def health_checkup_online():
    return render_template('health_checkup_online.html')

@app.route('/diabetespredict', methods=['POST'])
def diabetespredict():
    int_features  = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    output = round(prediction[0],2)
    print(type(output))
    return render_template('diabetesresult.html',prediction_text=output)

@app.route('/heartpredict', methods=['POST'])
def heartpredict():
    int_features  = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model1.predict(final_features)
    output = round(prediction[0],2)
    return render_template('heartresult.html',prediction_text=output)



@app.route('/cancerpredict', methods=['POST'])
def cancerpredict():
    int_features  = [float(x) for x in request.form.values()]
    print([type(int_features[0])])
    final_features = [np.array(int_features)]
    print([type(final_features[0])])
    print(final_features)
    prediction = model2.predict(final_features)
    print(type(prediction))
    return render_template('cancerresult.html',prediction_text=prediction)


@app.route('/payment',methods=['GET','POST'])
def make_payment():
    if request.method == "POST":
        email = request.form.get('email')
        name = request.form.get('name')
        purpose = request.form.get('purpose')
        amount = request.form.get('amount')
        user = User(email=email,name=name,purpose=purpose,amount=amount)
        db.session.add(user)
        db.session.commit()
        print(user.purpose)
        return redirect(url_for("pay",id=user.id))

    return render_template('payment_page.html')

@app.route('/pay/<id>',methods = ["GET","POST"])
def pay(id):
    user = User.query.filter_by(id=id).first()

    client = razorpay.Client(auth=("rzp_test_Gw4IVEcDgIy0iO","s0ed3WwDTwGtrGwqzJ3TqZOO"))
    payment = client.order.create({"amount":(int(user.amount) * 100),"currency":"INR","payment_capture":"1"})
    
    if request.method=="POST":
        return redirect(url_for("success", user_id = user.id))

    print(payment)    
    return render_template("pay.html", payment=payment,user_id = user.id)


@app.route('/success',methods = ['GET','POST'])
def success():
    # user = User.query.filter_by(id=id).first()
    # print(user)
    return render_template('success.html')   



if __name__ == '__main__':
    db.create_all()
    app.run(host='127.0.0.1', port=5000)