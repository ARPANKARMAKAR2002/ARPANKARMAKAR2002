from flask import Flask,render_template,request,jsonify
import pandas as pd
import pickle
app=Flask(__name__,template_folder='template')
car=pd.read_csv("Cleaned_Car.csv")
model=pickle.load(open("LinearRegressionModel.pkl",'rb'))
@app.route('/')

def index():
    companies=sorted(car['company'].unique())
    carmodels=sorted(car['name'].unique())
    year=sorted(car['year'].unique(),reverse=True)
    fuel_type=car['fuel_type'].unique()
    return render_template('index.html',companies=companies, carmodels=carmodels, years=year, fuel_type=fuel_type)

@app.route('/predict',methods=['POST'])

def predict():
    company=request.form.get('Company')
    car_model=request.form.get('car_model')
    year=int(request.form.get('Year'))
    fuel_type=request.form.get('Fuel')
    kms_driven=int(request.form.get('kilo_driven'))

    prediction=model.predict(pd.DataFrame([[car_model,company,year,kms_driven,fuel_type]],columns=['name','company','year','kms_driven','fuel_type']))
    print(int(prediction))
    return jsonify(int(prediction[0]))

# API endpoint for car models based on company selection
@app.route('/api/carmodels', methods=['GET'])
def get_car_models():
    company = request.args.get('company')

    # Filter car models based on the selected company
    filtered_models = car[car['company'] == company]['name'].unique()

    # Return JSON response with filtered car models
    return jsonify({'car_models': list(filtered_models)})

if __name__=='__main__':
    app.run(debug=True)