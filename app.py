from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler


app = Flask(__name__)
model = pickle.load(open('car_price_prediction.pkl', 'rb'))
@app.route('/', methods =['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel = 0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Kms_Driven2 = np.log(Kms_Driven)
        Owner = int(request.form['Owner'])
        fuel_type =request.form['fuel_type']
        if (fuel_type == 'Petrol'):
            fuel_type = 1
            Fuel_Type_Diesel = 0
        else:
            fuel_type = 0
            Fuel_Type_Diesel = 1
        Year = 2021-Year
        dealer_type = request.form['dealer_type']
        if dealer_type == "Individual":
            dealer_type = 1
        else:
            dealer_type = 0
        transmission_type = request.form['transmission_type']
        if transmission_type == 'Manual':
            transmission_type = 1
        else:
            transmission_type = 0
        prediction = model.predict([[Present_Price,Kms_Driven,Owner,Year,fuel_type,Fuel_Type_Diesel,dealer_type,transmission_type]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)