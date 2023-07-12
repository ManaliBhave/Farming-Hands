from flask import Flask, render_template, request, Markup
import numpy as np
import pandas as pd
import requests
import config
import pickle

crop_recommendation_model_path = 'models/rfc.pkl'
crop_recommendation_model = pickle.load(
    open(crop_recommendation_model_path, 'rb'))

def weather_fetch(city_name):
    """
    Fetch and returns the temperature and humidity of a city
    :params: city_name
    :return: temperature, humidity
    """
    api_key = config.weather_api_key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]

        temperature = round((y["temp"] - 273.15), 2)
        humidity = y["humidity"]
        return temperature, humidity
    else:
        return None

app = Flask(__name__)

@ app.route('/')
def home():
    title = 'Home'
    return render_template('index.html', title=title)

@ app.route('/crop-recommend')
def crop_recommend():
    title = 'Crop Recommendation'
    return render_template('crop.html', title=title)

@ app.route('/crop-predict', methods=['POST'])
def crop_prediction():
    title = 'Crop Recommendation'

    if request.method == 'POST':
        N = int(request.form['nitrogen'])
        P = int(request.form['phosphorous'])
        K = int(request.form['pottasium'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])
        city = request.form.get("city")

        if weather_fetch(city) != None:
            temperature, humidity = weather_fetch(city)
            data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
            my_prediction = crop_recommendation_model.predict(data)
            final_prediction = my_prediction[0]
        
        N = int(request.form['nitrogen']) - 15
        P = int(request.form['phosphorous']) - 15
        K = int(request.form['pottasium']) - 15
        ph = float(request.form['ph']) - 0.5
        rainfall = float(request.form['rainfall']) - 100
        city = request.form.get("city")

        if weather_fetch(city) != None:
            temperature, humidity = weather_fetch(city)
            data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
            my_prediction = crop_recommendation_model.predict(data)
            final_prediction1 = my_prediction[0]

        N = int(request.form['nitrogen']) - 10
        P = int(request.form['phosphorous']) - 10
        K = int(request.form['pottasium']) - 10
        ph = float(request.form['ph']) - 1
        rainfall = float(request.form['rainfall']) - 200
        city = request.form.get("city") 

        if weather_fetch(city) != None:
            temperature, humidity = weather_fetch(city)
            data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
            my_prediction = crop_recommendation_model.predict(data)
            final_prediction2 = my_prediction[0]
            
            if(final_prediction == final_prediction1 and final_prediction1 == final_prediction2):
                return render_template('crop-result.html', prediction=final_prediction, title=title)
            elif (final_prediction == final_prediction1 and final_prediction1 != final_prediction2):
                return render_template('crop-result.html', prediction=final_prediction, prediction1=final_prediction2, title=title)
            elif (final_prediction == final_prediction2 and final_prediction1 != final_prediction2):
                return render_template('crop-result.html', prediction=final_prediction, prediction1=final_prediction1, title=title)
            elif (final_prediction1 == final_prediction2 and final_prediction1 != final_prediction):
                return render_template('crop-result.html', prediction=final_prediction, prediction1=final_prediction1, title=title)
            elif(final_prediction != final_prediction1 and final_prediction1 != final_prediction2 and final_prediction != final_prediction2):
                return render_template('crop-result.html', prediction=final_prediction, prediction1=final_prediction1, prediction2=final_prediction2, title=title)        
            else:
                return render_template('try_again.html', title=title)
        else:
            return render_template('try_again.html', title=title)


@ app.route('/about-us')
def about_us():
    title = 'About Us'
    return render_template('about.html', title=title)

if __name__ == '__main__':
    app.run(debug=True)