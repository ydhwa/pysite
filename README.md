# 환경설정
## Version
- Python 3.7.3
## Library
- django
- psychpg2
   - 2.8.x

---

> 기본적으로 Django 프로젝트 한 개 당 한 개의 DB를 사용한다.
>
> Django 프로젝트에는 기본적으로 관리 프로그램이 내장되기 때문이다. 

# postgresql에 db 생성 및 계정 생성 접근 권한 부여
## 1. 새로운 데이터베이스 생성
`create database pysite;`

## 2. 새로운 사용자 추가
프로젝트마다 데이터베이스를 하나씩 추가해줘야 한다.

`create user pysite with password 'pysite';`

## 3. 테이블에 대한 권한 추가
`grant all privileges on all tables in schema public to pysite;`

## 4. `data/pg_hba.conf` 접근 설정

---

# Pycharm(community)에서 Django 프로젝트 시작하기
## 1. pycharm 프로젝트 생성(python_ch3 프로젝트)

## 2. Django 설치
### [터미널]
`pip install django`

## 3. Django 프로젝트 생성
### [터미널]
`django-admin startproject pysite`

## 4. 디렉터리 정리
pycharm 프로젝트와 django 프로젝트의 디렉터리를 일치시키는 작업

Pycharm의 터미널에서 실행하기 때문에 바로 Django 를 설치하는 과정에 비해 한 단계 더 하위 항목이 생긴다.

따라서, 하위 항목을 하나씩 위쪽으로 끌어올려준다. 

## 5. psycopg2 (postgres db lib 설치)
### [터미널]
`pip install psycopg2`

## 6. settings.py 설정
### 1) 시간대 변경
`TIME_ZONE = 'Asia/Seoul'`

### 2) 데이터베이스 변경
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pysite',
        'USER': 'pysite',
        'PASSWORD': 'pysite',
        'HOST': '192.168.1.48',
        'PORT': 5432,
    }
}
```

### 3) Template 디렉터리 설정
```python
TEMPLATES = [
    {
        ...
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        ...
    },
]
```

설정 후 pysite 프로젝트 바로 아래에 templates 디렉터리를 생성한다.

### 4) STATIC 디렉터리 설정 및 URL 매핑
```python
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'statics'),)
STATIC_URL = '/assets/'
```

## 7. Django 프로젝트의 기본 관리 어플리케이션이 사용하는 테이블을 생성
### [터미널]
`python manage.py migrate`

Django 어플리케이션과 물리적인 데이터베이스를 동기화 시키는 작업이다.

문제가 많이 발생하는 부분이다.

## 8. Django 프로젝트의 기본 관리 어플리케이션 로그인 계정 생성 (=관리 계정 생성)
### [터미널]
`python manage.py createsuperuser`

## 9. 지금까지 작업 내용 확인
### [터미널]
`python manage.py runserver 0.0.0.0:8888`

---

# Appliation 작업 진행
