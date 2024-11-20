from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.IntField(pk=True)
    tg_id = fields.BigIntField(unique=True)
    full_name = fields.CharField(max_length=255)
    username = fields.CharField(max_length=100, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
