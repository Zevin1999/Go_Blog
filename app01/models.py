from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
'''用户表'''
class UserInfo(AbstractUser):
    nid = models.AutoField(primary_key=True)
    #头像 FileFiled文件:varchar类型，default:默认值，upload_to上传的路径
    avatar = models.FileField(upload_to='avatar/', default='avatar/default.jpg')
    #和博客表一对一，OneToOneField本质是ForeignKey,但有唯一性约束unique=True
    # blog = models.ForeignKey(to='Blog', to_field='nid', null=True,unique=True)
    blog = models.OneToOneField(to='Blog', to_field='nid', null=True, on_delete=models.CASCADE)

    #元信息
    class Meta:
        #在admin中显示的表名
        verbose_name = "用户表"
        #去掉用户表后的sapp01_article
        verbose_name_plural = verbose_name
'''博客表'''
class Blog(models.Model):
    nid = models.AutoField(primary_key=True)
    #站点名称
    title = models.CharField(max_length=64)
    #站点名称副标题
    site_name = models.CharField(max_length=32)
    #主题
    theme = models.CharField(max_length=64)
    def __str__(self):
        return self.site_name
    class Meta:
        verbose_name = "博客表"
        verbose_name_plural = verbose_name

'''分类表'''
class Category(models.Model):
    nid = models.AutoField(primary_key=True)
    #分类名称
    title = models.CharField(max_length=64)
    #和博客表一对多关系，to 指定关联表  to_field 指定关联字段
    blog = models.ForeignKey(to='Blog', to_field='nid', null=True, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "分类表"
        verbose_name_plural = verbose_name
'''标签表'''
class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    #标签名称
    title = models.CharField(max_length=64)
    #和博客表一对多关系
    blog = models.ForeignKey(to='Blog', to_field='nid', null=True, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "标签表"
        verbose_name_plural = verbose_name

'''文章表'''
class Article(models.Model):
    nid = models.AutoField(primary_key=True)
    #verbose_name指定在admin中显示字段的名称
    title = models.CharField(max_length=64, verbose_name="文章标题")
    #文章摘要
    desc = models.CharField(max_length=255, verbose_name="文章摘要")
    #文章内容
    content = models.TextField()
    #文章创建时间
    #DateTimeField()年月日时分秒
    # auto_now_add插入数据会存入当前时间 auto_now修改数据会存入当前时间
    create_time = models.DateTimeField(auto_now_add=True)
    commit_num = models.IntegerField(default=0)
    up_num = models.IntegerField(default=0)
    down_num = models.IntegerField(default=0)
    # 和博客表一对多关系
    blog = models.ForeignKey(to='Blog', to_field='nid', null=True, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(to='Category', to_field='nid', null=True, on_delete=models.DO_NOTHING)
    tag = models.ManyToManyField(to='Tag', through='ArticleToTag', through_fields=('article', 'tag'))

    def __str__(self):
        return self.title+'----'+self.blog.userinfo.username
    class Meta:
        verbose_name = "文章表"
        verbose_name_plural = verbose_name

class ArticleToTag(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to='Article', to_field='nid', on_delete=models.DO_NOTHING)
    tag = models.ForeignKey(to='Tag', to_field='nid', on_delete=models.DO_NOTHING)


'''评论表'''
class Commit(models.Model):
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to='UserInfo', to_field='nid', on_delete=models.DO_NOTHING)
    article = models.ForeignKey(to='Article', to_field='nid', on_delete=models.DO_NOTHING)
    content = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    #自关联
    parent = models.ForeignKey(to='self', to_field='nid', null=True, blank=True, on_delete=models.DO_NOTHING)
    class Meta:
        verbose_name = "评论表"
        verbose_name_plural = verbose_name


'''点赞点踩表'''
class UpAndDown(models.Model):
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to='UserInfo', to_field='nid', on_delete=models.DO_NOTHING)
    article = models.ForeignKey(to='Article', to_field='nid', on_delete=models.DO_NOTHING)
    #bool类型
    is_up = models.BooleanField()
    #联合唯一
    class Meta:
        unique_together = (('user', 'article'),)
        verbose_name = "点赞点踩表"
        verbose_name_plural = verbose_name