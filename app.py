from flask import Flask,jsonify,request
import pickle
app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'name':'Hasani',
                    'status':'Server Working'})

#overall MMSE PREDICTION
#Load the trained model
model = pickle.load(open('predict_mmse_score_model.pkl', 'rb'))


@app.route('/predict', methods=['POST'])
def predict():
    # Get the input data from the request
    music_time = int(request.json['music_time'])
    physical_time = int(request.json['physical_time'])
    games_time = int(request.json['games_time'])

    # Make a prediction using the loaded model
    prediction = model.predict([[music_time, physical_time, games_time]])

    # Convert the prediction to an integer and return it as a JSON response
    mmse_score = float(round(prediction[0], 0))
    print(mmse_score)
    return jsonify(mmse_score=mmse_score), 200

#MUSIC RECOMMENDATION
music_model = pickle.load(open('predict_music_genres.pkl', 'rb'))

@app.route('/predict/genres', methods=['POST'])
def predictMusic():
    # Get the input data from the request
    gender = int(request.json['Gender'])
    age = int(request.json['Age'])
    educ = int(request.json['Educ'])
    mmse = int(request.json['MMSE'])

    # Make a prediction using the loaded model
    prediction = music_model.predict([[gender, age, educ, mmse]])

    # Convert the prediction to an integer and return it as a JSON response
    genres = int(prediction[0])
    print(genres)
    return jsonify(predicted_genres=genres),200

games_model = pickle.load(open('predict_game_level_model.pkl', 'rb'))
#GAME RECOMMENDATION
@app.route('/predict/gemes/level', methods=['POST'])
def predictGameLevel():
    # Get the input data from the request
    mmse = int(request.json['MMSE Score'])
    age = int(request.json['Age'])
    gameNum = int(request.json['Game Number'])


    # Make a prediction using the loaded model
    prediction = games_model.predict([[mmse, age, gameNum]])

    # Convert the prediction to an integer and return it as a JSON response
    level = int(prediction[0])
    print(level)
    return jsonify(predicted_games_level=level),200


#To change the port command
# python -m flask run -h localhost -p 3000
