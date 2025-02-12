from PyKakao import Message
import requests
import pandas as pd
import json
import math

# 메시지 API 인스턴스 생성
with open("Github/BIS/data/service_keys.json", "r") as f:
    service = json.load(f)
kakao_service_key = service["kakao_service_key"]
api_service_key = service["api_service_key"]
MSG = Message(kakao_service_key)

# 액세스 토큰 설정
with open("Github/BIS/data/full_response.json", "r") as f:
    config = json.load(f)
access_token = config["access_token"]
MSG.set_access_token(access_token)

data_url = f"https://apis.data.go.kr/6410000/busarrivalservice/v2/getBusArrivalListv2?format=json&serviceKey={api_service_key}&stationId=200000419"
response = requests.get(data_url)
contents = response.text
print(contents)

# JSON 파일에 저장
with open("Github/BIS/data/data.json", "w") as f:
    json.dump(contents, f)

# JSON 데이터 파싱
data = json.loads(contents)
# 'busArrivalList' 추출
arrival_list = data['response']['msgBody']['busArrivalList']
# DataFrame 생성
df = pd.DataFrame(arrival_list)
# DataFrame 정리 (빈 문자열 값을 NaN으로 변경)
df = df.replace('', pd.NA)
# 필요에 따라 컬럼 타입 변경 (예: predictTimeSec을 숫자형으로)
numeric_cols = ['predictTime1', 'predictTime2', 'predictTimeSec1', 'predictTimeSec2', 'crowded1', 'crowded2', 'locationNo1', 'locationNo2', 'lowPlate1', 'lowPlate2', 'remainSeatCnt1', 'remainSeatCnt2', 'routeId', 'routeTypeCd', 'staOrder', 'stationId', 'taglessCd1', 'taglessCd2', 'turnSeq', 'vehId1', 'vehId2', 'stateCd1', 'stateCd2']
for col in numeric_cols:
    if col in df.columns:  # 컬럼이 존재하는지 확인
        df[col] = pd.to_numeric(df[col], errors='coerce') # errors='coerce'는 숫자로 변환할 수 없는 값을 NaN으로 처리
cols = ['predictTime1', 'predictTime2', 'stationNm1', 'routeName']
subset_df = df[cols]
# DataFrame 출력
print(df)
print(subset_df)

# 또는 CSV 파일로 저장
subset_df.to_csv("Github/BIS/data/bus_arrival_data.csv", encoding="utf-8", index=True)
data_list = subset_df.to_numpy().tolist()
result = []
for i in data_list:
    if not (math.isnan(i[0])):
        result.append(i)
print(result)

# 1. 나에게 보내기 API - 텍스트 메시지 보내기 예시
message_type = "text" # 메시지 유형 - 텍스트
text = "테스트 메시지입니다.\n" # 전송할 텍스트 메시지 내용
for i in result:
    text += str(i[3]) + " 번 버스가 " + str(i[0]) + "분 후 도착 예정입니다.\n"
print(text)
link = {
  "web_url": "https://developers.kakao.com",
  "mobile_web_url": "https://developers.kakao.com",
}
button_title = "바로 확인" # 버튼 타이틀

MSG.send_message_to_me(
    message_type=message_type, 
    text=text,
    link=link,
    button_title=button_title,
)
