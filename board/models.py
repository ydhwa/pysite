from django.db import models
from django.utils import timezone
from django_enumfield import enum
from user.models import User


# Create your models here.
class BoardStatus(enum.Enum):
    ACTIVE = 0
    INACTIVE = 1

    labels = {
        ACTIVE: 'Active',
        INACTIVE: 'Inactive'
    }


class Board(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(default='')
    hit = models.IntegerField(default=0)
    regdate = models.DateTimeField(auto_now=True)
    groupno = models.IntegerField(default=0)
    orderno = models.IntegerField(default=0)
    depth = models.IntegerField(default=0)
    user = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)
    status = enum.EnumField(BoardStatus, default=BoardStatus.ACTIVE)

    def __str__(self):
        return f'Board({self.title}, {self.content}, {self.hit}, {self.regdate}, {self.groupno}, {self.orderno}, {self.depth}, {self.user})'


# 조회수 저장 테이블
class HitCount(models.Model):
    ip = models.CharField(max_length=15, default=None, null=True)
    post = models.ForeignKey(Board, default=None, null=True, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now(), null=True, blank=True)

    def __str__(self):
        return f'HitCount({self.ip}, {self.post}, {self.date})'
