import os
import json
from PIL import Image

import numpy as np
import tensorflow as tf
import streamlit as st

working_dir = os.path.dirname(os.path.abspath(__file__))
model_path = f"{working_dir}/trained_model/plant_model.h5"

#load the trained model
model =  tf.keras.models.load_model(model_path)

#loading the class model
class_indices = json.load(open(f"{working_dir}/class_indices.json"))

#function to load and preprocess the image using pillow

def load_and_preprocess_image(image_path, target_size= (224,224)):     #set the user's image shape to 224,224
  #load the image
  img = Image.open(image_path)
  #resize the image
  img = img.resize(target_size)
  #convert the image to numpy array
  img_array = np.array(img)
  #add batch dimension
  img_array = np.expand_dims(img_array, axis=0)
  #scale the image values to [0,1]
  img_array = img_array.astype('float32') / 255.

  return img_array

#function to predict the class of an image
def predict_image_class(model, image_path, class_indices):
  preprocessed_img = load_and_preprocess_image(image_path)
  predictions = model.predict(preprocessed_img)
  predicted_class_index = np.argmax(predictions, axis=1)[0]
  predicted_class_name = class_indices[str(predicted_class_index)]
  return predicted_class_name


#streamlit app

st.title('🌱 Plant Disease Identifier')

uploaded_image = st.file_uploader("Upload an image...", type=['jpg','png','jpeg'])

if uploaded_image is not None:
  image= Image.open(uploaded_image)
  col1, col2 = st.columns(2)
  with col1:
    resized_img = image.resize((150,150))  #just for displaying
    st.image(resized_img)
  
  with col2:
    if st.button('Identify'):
      #process the uploaded image and predict the result
      prediction = predict_image_class(model, uploaded_image, class_indices)
      st.success(f'Prediction: {str(prediction)}')

