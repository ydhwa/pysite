# board 구현
## 1. limit 처리
```python
start = (page - 1) * pagesize
Board.objects.all().order_by('-regdate')[start:start + pagesize]
```

## 2. insert
```python
board = Board()
board.title = '...'
...
...
board.user_id = '...'

board.save()

```

## 3. increase hit
```python
board = Board...
board.hit = board.hit + 1
board.save()

```

## 4. TotalCount
```python
# objects.all 절대 쓰지 마라. 진짜 다가져오느라 무리한다. 
Board.objects.count()
```