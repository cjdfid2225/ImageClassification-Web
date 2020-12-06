import boto3
from flask import Flask, render_template, request,jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import key_config as keys
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import requests
from PIL import Image
from io import BytesIO
#from module import dbModule
import query
import json

import plotly.graph_objs as go 

def plot_bar_ntr(name, value, f_name): 

    fig = go.Figure(
        data=[
            go.Bar(x=name, y=value, name="test")
        ]
    )
    fig.update_layout(title_text=f_name+'의 영양성분')

    json_str = fig.to_json() 
    return json.loads(json_str)





s3 = boto3.resource('s3')
bucket_name = "encore5-project"
bucket = s3.Bucket(name=bucket_name)

app = Flask(__name__)
CORS(app)
food_list = ['갈비구이', '감자전', '김밥', '김치볶음밥', '닭볶음탕', '도라지무침', '라볶이', '멍게', '백김치', '북엇국', '산낙지','생선전','알밥','오징어채볶음','콩국수']

model = load_model('./Model/best_model_15class.hdf5',compile = False)

def img_analysis(input_image_url):
    # key_name = input_image_name # 파일이름 
    url = input_image_url # 다운로드 주소 
    img = requests.get(url)
    img = Image.open(BytesIO(img.content))
    img = img.resize((299,299))
    img = image.img_to_array(img) 
    img = np.expand_dims(img, axis=0) 
    img /= 255.

    pred = model.predict(img)
    index = np.argmax(pred) 
    food_list.sort()
    pred_value = food_list[index]

    return pred_value


@app.route('/')  
def home():
    return render_template("file_upload_to_s3.html")

@app.route('/plot-plotly',methods=['post'])
def plot_plotly():
    if request.method == 'POST':
        print(request) 
    return jsonify({"status": True})

@app.route('/upload',methods=['post'])
def upload():
    if request.method == 'POST':
        img = request.files['file']
        # print(img)
        if img:
            filename = secure_filename(img.filename) # 파일명을 보호하기위한 함수.
            img.save(filename)
            s3.upload_file(
                Bucket = bucket_name, # 객체들이 모여있는 컨테이너?
                Filename=filename, 
                Key = "image/"+ filename # 저장되는 이름 경로 넣으려면 image/filename 이런식으로도 가능
            )
            msg = "Upload Done ! "
            # print(filename)
    return render_template("file_upload_to_s3.html",msg =msg)

@app.route("/process", methods=['GET', 'POST'])
def process():
    result = {}
    content = request.json
    # input_filename = content['analysis_filename']
    input_url = content['analysis_url']
    user_id =  content['analysis_id']
    result = img_analysis(input_url)

    result = {
        'modeling_result': result,
        "user_id": user_id,
    }

    food_name=result['modeling_result']
    u_id =result['user_id']

    conn = query.db_connect()
    
    try:
        info = query.get_foodinfo(conn, food_name)
        sql_result = query.insert_intake(conn, u_id, info)
        date = str(sql_result['date'])[:10]
        sumdata = query.sumbyDate(conn, user_id, date)
        

    finally:
        if conn:
            conn.close()
    
    # return jsonify(sql_result)
    
    # 바 그래프 그리기
    f_name = sql_result['food_name']
    name, val = list(), list() 
    for elem in sql_result: 
        if 'ntr' in elem: 
            name.append(elem) 
            val.append(sql_result[elem])

    # 누적 그래프 그리기
    name, val = list(), list()
    for elem in sumdata:
        if 'total' in elem:
            name.append(elem)
            val.append(sumdata[elem])

    res1 = plot_bar_ntr(name, val, f_name)
    res2 = plot_bar_ntr(name, val, date)
    print(jsonify(res1)) # 업로드한 음식의 영양분
    print(jsonify(res2)) # 업로드한 사람의 총 영양분
    fin_res = dict(
        res1=res1, 
        res2=res2
    ) 
    print(fin_res)

    # return '{} {}'.format(jsonify(res1), jsonify(res2))
    return jsonify(fin_res)

if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, threaded=True, debug=True)
