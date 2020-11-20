from flask import Flask, render_template
from flask import Flask, request, render_template
import numpy as np
import pickle
import math
app = Flask(__name__)
model = pickle.load(open('diabetesmodel.pkl','rb'))
model1 = pickle.load(open('heartmodel.pkl','rb'))
model2 = pickle.load(open('cancermodel.pkl','rb'))


@app.route("/")
def home():
    return render_template('home.html')

@app.route('/index')
def patient_page():
    return render_template('index.html')

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


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5500)