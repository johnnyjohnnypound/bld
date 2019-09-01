from django.db.models.signals import post_migrate
from .models import Debater

# 定义receiver函数
def init_db(sender, **kwargs):
    if sender.name == 'Debater.__name__':
        if not Debater.objects.exists():
            Debater.objects.create()        # 当发送信号的模型是你要初始化的模型的时候，在进行数据库操作，不加判断的话，每一个模型都会调用
 
post_migrate.connect(init_db)