import os
from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
from tensorflow.keras.models import load_model
from werkzeug import secure_filename
from tensorflow.keras.preprocessing import image
import numpy as np
import glob




app = Flask(__name__, static_folder='outputs')
food_list = ['갈비구이', '감자전', '김밥', '김치볶음밥', '닭볶음탕', '도라지무침', '라볶이', '멍게', '백김치', '북엇국', '산낙지','생선전','알밥','오징어채볶음','콩국수']
def prediction_class(model_best,images):
    for img in images:
        img = image.load_img(img, target_size=(299, 299))
        img = image.img_to_array(img) # 이미지를 numpy 배열로 전환해준다.
        img = np.expand_dims(img, axis=0) # 차원증가
        img /= 255.
    pred = model_best.predict(img)
    index = np.argmax(pred) # 예측값이 가장 높은
    food_list.sort()
    pred_value = food_list[index]
    # print(pred_value)
    return pred_value


@app.route("/upload")
def render_file():
    return render_template('upload.html')
@app.route('/prediction_class', methods=["GET","POST"])
def predict():
    # if request.method=="POST":
    #     f = request.files['file']
    #     f.save("./uploads/"+secure_filename(f.filename))
    model_best = load_model('../Data/kfood/best15_1/best_model_15class.hdf5',compile = False)
    images = glob.glob('./uploads/*.jpg')
    # print(type(images))
    # return prediction_class(model_best,images)
    return str(prediction_class(model_best, images) )
if __name__ == '__main__':
    app.run('0.0.0.0', port=80, threaded=True) # 처리 속도 향상을 위해 쓰레드를 적용합니다.