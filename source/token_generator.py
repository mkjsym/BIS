from PyKakao import Message
import json

# 메시지 API 인스턴스 생성
MSG = Message(service_key = "8d64b5119f06ed97c3551469998e2f17")

# 카카오 인증코드 발급 URL 생성
auth_url = MSG.get_url_for_generating_code()
print(auth_url)

# 카카오 인증코드 발급 URL 접속 후 리다이렉트된 URL
url = input("위 링크에 접속한 후 로그인하여 리다이렉트 된 URL을 입력하세요: ")

# 위 URL로 액세스 토큰 추출
full_response, access_token = MSG.get_access_token_by_redirected_url(url)
# JSON 파일에 저장
with open("BIS/data/full_response.json", "w") as f:
    json.dump(full_response, f)
print(access_token)
