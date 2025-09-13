""" 定义数据模型Data Models，相当于数据库蓝图 """

from tortoise import fields,models

# 用户表
class Users(models.Model): 
    id = fields.IntField(pk=True) #主键字段，唯一标识每个用户
    username = fields.CharField(max_length=20, unique=True) #用户名，最长为20字符，不能重复
    full_name = fields.CharField(max_length=50,null=True) #可选字段
    password = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True) #只在创建时自动设置为当前时间
    modified_at = fields.DatetimeField(auto_now = True) #每次保存时自动更新为当前时间
    
# 笔记表
# author作为外键，与用户是一对多的关系，一个用户可以创建多条笔记
class Notes(models.Model):
    id = fields.IntField(pk=True) #主键
    title = fields.CharField(max_length = 225)
    content = fields.TextField()
    author = fields.ForeignKeyField("models.use",related_name="note") #elated_name允许用户对象反向查询其所有笔记，比如user.note.all()
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title},{self.author_id} on {self.created_at}"