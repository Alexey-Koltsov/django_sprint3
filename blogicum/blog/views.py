from blog.models import Category, Post
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.utils import timezone


def index(request):
    posts = Post.objects.select_related('category', 'location').filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    ).order_by('-pub_date')[:5]
    context = {'post_list': posts}
    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    posts = get_object_or_404(
        Post.objects.select_related('category', 'location').filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
        ),
        pk=id
    )
    context = {'post': posts}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    categories = get_object_or_404(
        Category.objects.values('title', 'description'),
        slug=category_slug
    )
    posts = get_list_or_404(
        Post.objects.only(
            'pub_date',
            'title',
            'location',
            'author',
            'text',
            'category__slug',
            'category__title',
        ).filter(
            category__slug=category_slug,
            is_published=True,
            pub_date__lte=timezone.now(),
        ).order_by('-pub_date'),
        category__is_published=True
    )
    context = {
        'post_list': posts,
        'category': categories,
    }
    return render(request, 'blog/category.html', context)
