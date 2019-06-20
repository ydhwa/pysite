# guestbook 구현
## 구현
### 1. model
### 2. /guestbook/delete/10
`urls.py`
```python
path('helloworld/hello2/<int:id>', helloworld_views.hello2),
```

`views.py`
```python
def hello2(request, id=0):
    return HttpResponse(f'id: {id}')
```

### 3. orm method
- index(list): ok
- add: ok
- delete
   repository 에서 객체를 영속화
    ```python
    guestbook = Guestbook.objects.filter(id=20).filter(password='1234')
    guestbook.delete()
    ``` 

## 구현 안해도 되는 것
`list.html` 템플릿에서
1. 메시지 index 잡는 것 하지 말 것
   - django template arith operation
   - <https://docs.djangoproject.com/en/2.2/ref/templates/builtins/>
2. 메시지 개행문자 <br> replace 하지 말 것
   - hint: filter