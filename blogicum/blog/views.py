from django.shortcuts import get_list_or_404, get_object_or_404, render

from blog.models import Category, Post

from django.db.models import Q

from django.utils import timezone


def index(request):
    template = 'blog/index.html'
    posts = Post.objects.select_related('category', 'location').filter(
        Q(pub_date__lte=timezone.now()) &
        Q(is_published=True) &
        Q(category__is_published=True)
    ).order_by('-pub_date')[:5]
    context = {'post_list': posts}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    posts = get_object_or_404(
        Post.objects.select_related('category', 'location').filter(
            Q(pub_date__lte=timezone.now()) &
            Q(is_published=True) &
            Q(category__is_published=True)
        ),
        pk=id
    )
    context = {'post': posts}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    categories = get_object_or_404(
        # Первый аргумент - QuerySet:
        Category.objects.values('title', 'description'),
        # Второй аргумент - условие,
        # по которому фильтруются записи из QuerySet:
        slug=category_slug
    )
    posts = get_list_or_404(
        Post.objects.select_related('category').filter(
            Q(category__slug=category_slug) &
            Q(is_published=True) &
            Q(pub_date__lte=timezone.now())
        ).order_by('-pub_date'),
        category__is_published=True
    )
    context = {
        'post_list': posts,
        'category': categories,
    }
    return render(request, template, context)
