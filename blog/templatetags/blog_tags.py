from django import template
from django.db.models import Count

from ..models import Post, Category, Tag

register = template.Library()

@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]

@register.simple_tag
def archives():#归档
    """
    这里 dates 方法会返回一个列表，列表中的元素为每一篇文章（Post）的创建时间，
    且是 Python 的 date 对象，精确到月份，降序排列。接受的三个参数值表明了这些含义，
    一个是 created_time ，即 Post 的创建时间，month 是精度，order='DESC' 表明降序排列
    （即离当前越近的时间越排在前面）。例如我们写了 3 篇文章，
    分别发布于 2017 年 2 月 21 日、2017 年 3 月 25 日、2017 年 3 月 28 日，
    那么 dates 函数将返回 2017 年 3 月 和 2017 年 2 月这样一个时间列表，且降序排列，
    从而帮助我们实现按月归档的目的。
    :return:
    """
    return Post.objects.dates('created_time', 'month', order='DESC')

@register.simple_tag
def get_tags():
    # 记得在顶部引入 Tag model
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

@register.simple_tag
def get_categories():
    # 记得在顶部引入 count 函数
    # Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
'''
这个 Category.objects.annotate 方法和 Category.objects.all 有点类似，
它会返回数据库中全部 Category 的记录，但同时它还会做一些额外的事情，
在这里我们希望它做的额外事情就是去统计返回的 Category 记录的集合中每条记录下的文章数。
代码中的 Count 方法为我们做了这个事，它接收一个和 Categoty 相关联的模型参数名
（这里是 Post，通过 ForeignKey 关联的），然后它便会统计 Category 记录的集合中每条记录下的与之关联的 
Post 记录的行数，也就是文章数，最后把这个值保存到 num_posts 属性中。

此外，我们还对结果集做了一个过滤，使用 filter 方法把 num_posts 的值小于 1 的分类过滤掉。
因为 num_posts 的值小于 1 表示该分类下没有文章，没有文章的分类我们不希望它在页面中显示。




此外，annotate 方法不局限于用于本文提到的统计分类下的文章数，你也可以举一反三，只要是两个 model 
类通过 ForeignKey 或者 ManyToMany 关联起来，那么就可以使用 annotate 方法来统计数量。
比如下面这样一个标签系统：

class Post(models.Model):
    title = models.CharField(max_length=70)
    body = models.TextField()
    Tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=100)
统计标签下的文章数：

from django.db.models.aggregates import Count
from blog.models import Tag

# Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
tag_list = Tag.objects.annotate(num_posts=Count('post'))
关于 annotate 方法官方文档的说明在这里：annotate。同时也建议了解了解 objects 下的其它操作数据库的方法，
以便在遇到相关问题时知道去哪里查阅。
'''

