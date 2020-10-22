# 식품영양성분db, 권장섭취기준

2020.10.22 진행상황

- db_api.py : 파일을 실행하면 식약처 식품영양성분DB(NEW)에서 데이터를 가져옴
  + 필요해보이는 컬럼을 추렸으나 혹 추후에 필요할 때를 대비해 원본 데이터도 저장해 두도록 코드를 작성했음



- recommend.json : 성별 및 연령대 기준 권장섭취기준을 찾아서 json파일로 작성함
  + 간략한 표(식품영양성분_자료집(2020)_table)와 세부적인 표(2015_한국인_영양소_섭취기준(원본)_20190514_9-15p)가 있어서 어떤 걸 기준으로 쓸지 선택해야 함
  + 이 파일은 간략한 표를 기준으로 작성했음
  + {성별 : {연령대 : { 영양성분군 : {영양소 : 권장섭취량} }}}  ** 이 형식으로 작성하는게 맞는지도 확인 필요



- DB에 필요한 테이블 논리모형 작성 + 테이블의 연결 관계나 더 필요한 사항은 없는지 확인 필요

user (_userid_, username, usergender, userage, userweight)

food_nutrition (food_code, food_name, serving_size, nutition1-9)	+ food_group

take_recommend (_gender_, _age_, _weight_? >> 조건에 따른 영양소별 권장 섭취량)	 ** 이 부분을 어떻게 작성해야 할지 난감

user_intake (_userid_, _date_, food_name, intake_nutrition1-9)
