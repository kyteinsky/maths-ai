from flask import Flask, render_template, session, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import TextField,SubmitField
from wtforms.validators import NumberRange
import numpy as np 
from tensorflow.keras.models import load_model
import joblib

def return_prediction(model, d_json):
 
    a = d_json['a']
    b = d_json['b']
    c = d_json['c']

    class_ind = model.

    return classes[class_ind][0]
