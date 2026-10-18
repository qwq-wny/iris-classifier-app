"""Tests for the web pages of the app."""

import pytest

from app.main import app


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_page_works(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Iris Flower Predictor" in response.data


def test_health_works(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


@pytest.mark.parametrize(
    "values,expected",
    [
        ((5.1, 3.5, 1.4, 0.2), "setosa"),
        ((5.9, 2.8, 4.3, 1.3), "versicolor"),
        ((7.2, 3.0, 5.8, 1.6), "virginica"),
    ],
)
def test_predict_real_flowers(client, values, expected):
    response = client.post(
        "/predict",
        data={
            "sepal_length": values[0],
            "sepal_width": values[1],
            "petal_length": values[2],
            "petal_width": values[3],
        },
    )
    assert response.status_code == 200
    assert f"Prediction: <b>{expected}</b>".encode() in response.data


def test_predict_with_a_missing_number(client):
    response = client.post(
        "/predict",
        data={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
        },
    )
    assert response.status_code == 200
    assert b"Please fill all 4 boxes with numbers." in response.data


def test_predict_with_words_not_numbers(client):
    response = client.post(
        "/predict",
        data={
            "sepal_length": "abc",
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
        },
    )
    assert response.status_code == 200
    assert b"Please fill all 4 boxes with numbers." in response.data


@pytest.mark.parametrize("bad_value", [-1, 0, 99])
def test_predict_with_numbers_out_of_range(client, bad_value):
    response = client.post(
        "/predict",
        data={
            "sepal_length": bad_value,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
        },
    )
    assert response.status_code == 200
    assert b"must be between 0 and 30 cm" in response.data
