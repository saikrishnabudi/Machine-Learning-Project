from flask import Flask, request, render_template
from src.pipeline.predict_pipeline import CustomData, PredictPipeline
from src.exception import CustomException

application = Flask(__name__)
app=application

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        try:
            data = CustomData(
                gender=request.form.get('gender', ''), 
                race_ethnicity=request.form.get('ethnicity', ''), 
                parental_level_of_education=request.form.get('parental_level_of_education', ''), 
                lunch=request.form.get('lunch', ''), 
                test_preparation_course=request.form.get('test_preparation_course', ''), 
                writing_score=float(request.form.get('writing_score', 0)),  # type: ignore
                reading_score=float(request.form.get('reading_score', 0)) # type: ignore
            )

            pred_df = data.get_data_as_data_frame()

            predict_pipeline = PredictPipeline()
            results = predict_pipeline.predict(pred_df)
            results[0] = min(results[0], 100)
            return render_template('home.html', results=results[0])

        except CustomException as e:
            # Handle custom exceptions
            error_message = str(e)
            return render_template('error.html', error_message=error_message)

        except Exception as e:
            # Handle other exceptions
            error_message = "An error occurred. Please try again later."
            return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)



        


