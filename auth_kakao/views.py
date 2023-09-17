from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse
# Create your views here.
CLIENT_ID = "0415290999a69e21e3ebf321013ad2f7"
REDIRECT_URI = "http://127.0.0.1:8000/kakao/callback"
def get_authorize_code(request):
    kauth_url = "https://kauth.kakao.com/oauth/authorize"

    # 인증 코드를 얻기 위한 파라미터 설정
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",  # 인증 코드를 얻기 위해 code를 사용합니다.
    }

    # Kakao 계정 로그인 페이지로 리다이렉트
    redirect_url = f"{kauth_url}?client_id={params['client_id']}&redirect_uri={params['redirect_uri']}&response_type={params['response_type']}"
    return redirect(redirect_url)

def callback(request):
    code = request.GET.get('code')
    data = {'grant_type': 'authorization_code',
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            'code': code  # 받은 인가 코드
            }
    headers = {'Contents-type': 'application/x-www-form-urlencoded;charset=utf-8'}
    res = requests.post('https://kauth.kakao.com/oauth/token', data=data,
                        headers=headers)  # import request해야한다, request package 설치 필요, res는 응답 받은 객체 이다
    token_json = res.json()  # json 파일로 받아온다
    access_token = token_json['access_token']  # access_token 받아오기

    # token
    headers = {'Authorization': 'Bearer ' + access_token,
               'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'}

    res = requests.get('https://kapi.kakao.com//v2/user/me', headers=headers)
    profile_res = res.json()
    nickname = profile_res['kakao_account']['profile']['nickname']

    return JsonResponse({"data":nickname})