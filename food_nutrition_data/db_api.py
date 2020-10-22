import os
import sys
import json
import urllib.request

# "MSG": "데이터요청은 한번에 최대 1000건을 넘을 수 없습니다.",
# "total_count": "29279",

start = [str(n) for n in range(1,29280, 1000)]
end = [str(j) for j in range(1000, 30001, 1000)]


# api에서 데이터 불러오기
for k in range(len(end)):
    
    url = "http://openapi.foodsafetykorea.go.kr/api/e1521f6c3d9e4d68b209/I2790/json/"+start[k]+"/"+end[k]
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)

    data = json.load(response)
    # 원본 데이터 저장하기
    with open('nutrition_db_'+start[k]+'-'+end[k]+'.json', 'w', encoding='utf-8') as make_file:
        json.dump(data, make_file, indent="\t", ensure_ascii=False)

    # 필요 없는 컬럼 버리기...  ## 혹시 필요한데 빼버린 데이터는 없는지 같이 확인할 것
    row_data = data['I2790']['row']
    trimed_data = []
    for i in range(len(row_data)):
        temp = {}
        temp['NUM'] = row_data[i]['NUM']    # 번호
        temp['FOOD_CD'] = row_data[i]['FOOD_CD']    # 식품코드
        temp['DESC_KOR'] = row_data[i]['DESC_KOR']  # 식품명
        temp['SERVING_SIZE'] = row_data[i]['SERVING_SIZE']  # 총내용량
        temp['NUTR_CONT1'] = row_data[i]['NUTR_CONT1']  # 열량(kcal)(1회제공량당)
        temp['NUTR_CONT2'] = row_data[i]['NUTR_CONT2']  # 탄수화물(g)(1회제공량당)
        temp['NUTR_CONT3'] = row_data[i]['NUTR_CONT3']  # 단백질(g)(1회제공량당)
        temp['NUTR_CONT4'] = row_data[i]['NUTR_CONT4']  # 지방(g)(1회제공량당)
        temp['NUTR_CONT5'] = row_data[i]['NUTR_CONT5']  # 당류(g)(1회제공량당)
        temp['NUTR_CONT6'] = row_data[i]['NUTR_CONT6']  # 나트륨(mg)(1회제공량당)
        temp['NUTR_CONT7'] = row_data[i]['NUTR_CONT7']  # 콜레스테롤(mg)(1회제공량당)
        temp['NUTR_CONT8'] = row_data[i]['NUTR_CONT8']  # 포화지방산(g)(1회제공량당)
        temp['NUTR_CONT9'] = row_data[i]['NUTR_CONT9']  # 트랜스지방(g)(1회제공량당)
        trimed_data.append(temp)

    with open('trimed_data'+start[k]+'-'+end[k]+'.json', 'w', encoding='utf-8') as make_file:
        json.dump(trimed_data, make_file, indent="\t",ensure_ascii=False)