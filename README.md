![header](https://capsule-render.vercel.app/api?type=rect&color=gradient&height=200&section=header&text=Connects&fontAlign=50&fontSize=70)
<div align="center"> 
 
# Connects API Backend
</div>

## 개요
- 선, 후배 간의 스터디, 프로젝트 협업, 공모전 참가를 보조하기 위한 서비스 Connects 입니다.
- Connects 서비스의 API 서버로 사용자 인증, 액티비티, 챕터의 관리를 수행합니다.
 
## First Install
```bash
git clone https://github.com/CASPER-REPSAC/casper-api.git
cd ./casper-api
python3 -m virtualenv venv
source ./venv/bin/activate
pip3 install -r requirements.txt

Do First Setting

python3 manage.py createsuperuser
python3 manage.py makemigrations
python3 manage.py migrate --run-syncdb
python3 manage.py runserver

Do Social Sites Setting
``` 

## First Setting
0. You need Google API Client ID and Client Key
1. Move to connects Directory
2. Make keys.json
3. Move back to Connects Root Directory
4. Make 'file' directory
5. Make 'logs' directroy

```
## keys.json
{
    "settings-secret-key" : "c1:6~tX4*m/ym*.WP2_,LN_4OLV(j!P/w_X{yZjWbc$T}fA?!E",

    "default-database-ENGINE" :"Your_Django_DB_Engine",
    "default-database-NAME" :"Your_Django_DB_Name",
    "default-database-USER" :"Your_Django_DB_Account",
    "default-database-PASSWORD" :"Your_Django_DB_PW",
    "default-database-HOST" :"Your_Django_DB_Host_eg_localhost", 
    "default-database-PORT" :"Your_Django_DB_Default_3306",

    "social_auth_google_client_id" : "Your_Google_API_Client_ID",
    "social_auth_google_secret":"Your_Google_API_Client_Key",
    "state":"Random_String_Or_Key_What_You_Want",
    
    "STATE" : "Random_String_Or_Key_What_You_Want"
}

```


## Social Sites Setting
1. Start Connects API Server
2. Move to admin page and sign using superuser
```
http://127.0.0.1:8000/admin
```
3. Click 'Sites' tab and add your domain
4. Click 'Social application' and add you Google API Client Key, Client Id and Site(step 3)
 
## 스택
<p align="left">
<img src="https://img.shields.io/badge/Python3-054480?style=flat-square&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Django-18ba1e?style=flat-square&logo=django&logoColor=white"/>
<img src="https://img.shields.io/badge/MySQL-12a5ff?style=flat-square&logo=mysql&logoColor=white"/>
</p>

## 프론트엔드
- 프론트엔드는 아래의 링크에서 확인하세요.
- [Frontend](https://github.com/CASPER-REPSAC/connect-frontend)

## 기능
### 0. URI 문서
- [API 요청 URI](https://www.notion.so/floodnut/Connects-API-64005bb57a964411afb8517cf5f8c231)

### 1. Social Auth
- Provider Google
- JWT를 통한 사용자 인증

### 2. 액티비티 CRUD 및 관리
- 챕터는 활동을 대분류로 나눈 것으로 Project, Study, CTF를 지원합니다.
- 액티비티 별 태그 추가와 참가, 탈퇴를 지원합니다.
- 챕터를 작성하여 액티비티를 보다 작은 단위로 관리할 수 있습니다.

### 3. 챕터 CRUD
- 챕터를 작성하고 활동의 세부적인 내용을 관리해보세요.
- 챕터에는 누구나 댓글을 통해 의견을 남길 수 있습니다.

## 버그, 오류 제보 및 제안
이슈를 통해 부탁드립니다.
