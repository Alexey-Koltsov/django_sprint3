from django.shortcuts import get_object_or_404, render

from blog.models import Post

from django.db.models import Q

from django.utils import timezone


def index(request):
    template = 'blog/index.html'
    posts = Post.objects.select_related('category').filter(
        Q(created_at__lte=timezone.now()) &
        Q(is_published=True) &
        Q(category__is_published=True)
    ).order_by('-pub_date')[:5]
    context = {'post_list': posts}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    if id >= len(posts):
        raise ValueError(f'Пост номер {id} не существует')
    context = {'post': posts[id]}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    context = {'category': category_slug}
    return render(request, template, context)
