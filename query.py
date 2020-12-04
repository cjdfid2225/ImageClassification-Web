import os
import sys
import json
import pymysql
from pymysql import DATE, NULL


# DB에 연결하는 함수
def db_connect():
    conn = pymysql.connect(
    user='',
    passwd='',
    host = "",
    db='project',
    charset='utf8',
    autocommit=True)
    return conn

# 식품 영양성분을 받아오는 함수
def get_foodinfo(conn, f_name):
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = 'select * from food_nutritions_modifed where food_name like %s'
        food_name = '%'+str(f_name)+'%'
        cursor.execute(sql, food_name)
        food_info = cursor.fetchall() # fetch all row , another func -> fetchone()
        print(food_info)
    cursor.close()
    return food_info


## 로그인 정보를 통해 유저정보를 가져오는 함수
def get_userinfo(conn, user_id):
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = 'select user_sex, user_age from user_info where user_id = %s'
        cursor.execute(sql, user_id)
        # 유저의 성별과 나이 변수화
        user_info = cursor.fetchone()
        
        print(user_info)
        user_sex = user_info['user_sex']
        user_age = user_info['user_age']
    cursor.close()

    return user_sex, user_age

# 섭취기준을 가져오는 함수
def get_recom(conn, user_sex, user_age):
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = 'select * from simple_recom where bySex = %s and %s between byAgeStart and byAgeEnd'
        cursor.execute(sql, (user_sex, user_age))
        recom = cursor.fetchone()
        cursor.close()
        return recom

# 섭취정보 저장
def insert_intake(conn, user_id, food_info):
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        # 받아온 데이터를 유저 정보랑 엮어서 저장하기
        # 이미지 분석 모델에서 분석값이 나오면 바로 db에 저장해주는 걸로!

        user_id = user_id
        food_num = food_info[0]['food_num']
        food_name = food_info[0]['food_name']
        food_servesize = food_info[0]['food_servesize']
        ntr1 = food_info[0]['ntr1_calorie']
        ntr2 = food_info[0]['ntr2_carbon']
        ntr3 = food_info[0]['ntr3_protein']
        ntr4 = food_info[0]['ntr4_fat']
        ntr5 = food_info[0]['ntr5_sugars']
        ntr6 = food_info[0]['ntr6_sodium']
        ntr7 = food_info[0]['ntr7_cholesterol']
        ntr8 = food_info[0]['ntr8_saturatedFat']
        ntr9 = food_info[0]['ntr9_transFat']

        sql = "insert into user_intake(user_id,food_num, food_name, food_servesize, \
            ntr1_calorie, ntr2_carbon, ntr3_protein, ntr4_fat, ntr5_sugars, ntr6_sodium, \
                ntr7_cholesterol, ntr8_saturatedFat, ntr9_transFat) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        data = (user_id, food_num, food_name, food_servesize, ntr1, ntr2, ntr3, ntr4, ntr5, ntr6, ntr7, ntr8, ntr9)
        cursor.execute(sql, data)
        
        inserted_id = conn.insert_id()
        sql_2 = 'select * from user_intake where record_id = %s'
        cursor.execute(sql_2, inserted_id)
        result = cursor.fetchone()

        return result


# 섭취 상태 평가 (탄단지 비율, 과다섭취 or 섭취부족)

# 날짜별 누적데이터 가져오기
def sumbyDate(conn, user_id, date):
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "select * from view_test4 where user_id = %s and DATE(date) = %s"
        cursor.execute(sql, (user_id, date))    
        result = cursor.fetchone()

        # 특정 날짜를 지정하고 싶으면 다음 내용으로! 파라미터에도 date 지정해주어야 함
        # sql = "select * from view_test4 where user_id = %s and DATE(date) = %s"
        # cursor.execute(sql, (user_id, date))
        # result = cursor.fetchone()

        cursor.close()
        return result

# 누적데이터 평가
def calbyDate(conn, user_id, date):
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        
        # user_id로 유저정보 가져오기
        user_sex, user_age = get_userinfo(conn, user_id)

        # 위의 정보와 엮어서 추천 기준 가져오기
        recom = get_recom(conn, user_sex, user_age)
        print(recom)
        
        # 유저아이디와 날짜별로 user_intake의 정보를 가져오기
        result = sumbyDate(conn, user_id)

        menu = result[-1]['total_menu'].split(',')
        total_calories = result[-1]['total_calorie']
        total_carbon = result[-1]['total_carbon']
        carbon_percentage = total_carbon*4 / total_calories * 100
        total_protein = result[-1]['total_protein']
        protein_percentage = total_protein*4 / total_calories * 100
        total_fat = result[-1]['total_fat']
        fat_percentage = total_fat*9 / total_calories * 100

        # if total_calories > energy: warning = "영양섭취 과다"
        # elif total_calories == energy: warning = "적당한 영양섭취"
        # else: warning = "영양섭취 부족"

        analysis_result = {
            "menu" : menu,
            "total_carbon" : total_carbon,
            "carbon_percentage" : carbon_percentage,
            "total_protein" : total_protein,
            "protein_percentage" : protein_percentage,
            "total_fat" : total_fat,
            "fat_percentage" : fat_percentage
        }

        return analysis_result 

#         (warning, "오늘 먹은 음식은 ", total_menu, "입니다. 총 칼로리는 ", total_calories, "이며", 
#             "탄수화물 비율은 ", carbon_percentage, "%, 단백질 비율은 ", protein_percentage, "%, 지방 비율은 ", fat_percentage "%입니다.")
            ## 이 부분을 json데이터로 만들어서 시각화할 수 있도록 던져주기!


# 추천음식      추천의 근거...      "복잡한 로직" /   전문가의 의견... / 누적된 옛날 데이터와의 비교    >>>     앞으로 우리의 과제...ㅎㅎ

# 영양제 추천?



if __name__ == "__main__":
    conn = db_connect()
    # user_sex, user_age = get_userinfo(conn, 'newbee')
    # recom = get_recom(conn, user_sex, user_age)
    # print(recom)

    # food_info = get_foodinfo(conn, '김치볶음밥')
    # result = insert_intake(conn, 'newbee', food_info)
    # print(result)

    try:
        info = get_foodinfo(conn, '김치볶음밥')
        sql_result = insert_intake(conn, 'newbee', info)
        date = str(sql_result['date'])[:10]
        print(date)
        result = sumbyDate(conn, 'newbee')
        print(type(result))
        a = calbyDate(conn, 'newbee', date)
        print('calbyDate 결과 :', a)
        print()

    finally:
        conn.close()
