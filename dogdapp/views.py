import requests
import json

from django.http import HttpResponseRedirect
from django.utils.dateformat import DateFormat
from datetime import datetime
from django.shortcuts import render
from django.views.generic import View
from .forms import oauthForm
from .models import oauth
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
class mainView(View):

    form_class = oauthForm
    initial = {'key': 'value'}
    template_name = 'dogdapp/main.html'

    def get(self, request):

        if (request.GET.get('code')):
            # return HttpResponse(request.GET.get('code'))
            code = request.GET.get('code')
            url = 'https://kauth.kakao.com/oauth/token'

            headers = {'Content-type': 'application/x-www-form-urlencoded; charset=utf-8'}

            body = {'grant_type': 'authorization_code',
                    'client_id': '448844327114515aa2e08f9cbf79a49a',
                    'redirect_uri': 'http://49.174.123.151:8000/',
                    'code': code}

            # return HttpResponse(f'{body}')
            kakao_response = requests.post(url, headers=headers, data=body)
            # return HttpResponse(f'{kakao_response.text}')

            access_token = json.loads(kakao_response.text).get('access_token')

            url = 'https://kapi.kakao.com/v2/user/me'

            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-type': 'application/x-www-form-urlencoded; charset=utf-8'
            }

            kakao_response = requests.get(url, headers=headers)

            data = {
                'id': json.loads(kakao_response.text).get('id'),
                'nickname': json.loads(kakao_response.text).get('properties').get('nickname'),
                'reg_date': DateFormat(datetime.now()).format('Y-m-d')
            }

            print(data)

            login_check = oauth.objects.filter(id=data['id']).values()
            print(login_check)

            if (len(login_check) == 0):
                form = self.form_class(data)
                oauth_save = form.save(commit=False)  # oauth란 이름으로 모델을 가져왔으므로 변수명을  oauth로 똑같이 쓸수 없음.
                oauth_save.save()
                request.session['id'] = data['id']
                request.session['nickname'] = data['nickname']
                return HttpResponseRedirect("/")
            else:
                request.session['id'] = data['id']
                request.session['nickname'] = data['nickname']
                return HttpResponseRedirect("/")
        else:
            return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)