"""Small web app that predicts the type of an iris flower."""

from flask import Flask, render_template, request

from app.predict import predict_iris

app = Flask(__name__)


@app.route("/")
def home():
    """Show the page with the input form."""
    return render_template("index.html", prediction=None, error=None)


@app.route("/predict", methods=["POST"])
def predict():
    """Read the 4 numbers from the form and predict the flower type."""
    try:
        sepal_length = float(request.form["sepal_length"])
        sepal_width = float(request.form["sepal_width"])
        petal_length = float(request.form["petal_length"])
        petal_width = float(request.form["petal_width"])
    except (KeyError, ValueError):
        message = "Please fill all 4 boxes with numbers."
        return render_template("index.html", prediction=None, error=message)

    try:
        flower = predict_iris(sepal_length, sepal_width, petal_length, petal_width)
    except ValueError as error:
        return render_template("index.html", prediction=None, error=str(error))

    return render_template("index.html", prediction=flower, error=None)


@app.route("/health")
def health():
    """Simple check that the app is running."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
