import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from milk.models import Post, Image, Page
from milk.forms import PostForm, ImageForm, PageForm
from milk.serializer import Serializer

User = get_user_model()

@login_required
def index(request):
    posts = Post.objects.filter().order_by('-created_at')[:10]
    context = {}
    context['posts'] = []
    for post in posts:
        context['posts'].append(Serializer.post(post))
    return render(request, 'milk/manage.html', context)

@login_required
def post(request, id):
    post = get_object_or_404(Post, pk=id)
    context = {}
    context['post'] = Serializer.post(post)
    return render(request, 'milk/post.html', context)


@login_required
def post_edit(request, id):
    post = get_object_or_404(Post, pk=id)
    context = {}
    context['post'] = Serializer.post(post)
    return render(request, 'milk/create.html', context)

@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, pk=id)
    post.delete()
    return redirect('milk:post_index')

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post_id = request.POST.get('post_id', None)
            if post_id is None:
                post = form.save(commit=False)
                post.author = request.user
                post.published = True
                post.save()
            else:
                post = get_object_or_404(Post, pk=post_id)
                post.title = form.cleaned_data['title']
                post.body = form.cleaned_data['body']
                post.save()
            return redirect('milk:post_index')
    return render(request, 'milk/create.html')

@login_required
def media(request):
    images = Image.objects.filter().order_by('-created_at')
    context = {}
    context['images'] = []
    for image in images:
        context['images'].append(Serializer.image(image))
    return render(request, 'milk/media.html', context)

@login_required
def add_media(request):
    return add_media_handler(request, 'HTML')

@login_required
def add_media_api(request):
    return add_media_handler(request)

@login_required
def media_delete(request, id):
    image = get_object_or_404(Image, pk=id)
    image.delete()
    return redirect('milk:media_index')

def add_media_handler(request, format='JSON'):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.uploader = request.user
            image.save()
            if format == 'JSON':
                path = os.path.join(settings.MEDIA_URL, str(image.image))
                if path[0] == '/':
                    path = path[1:]
                print(path)
                return JsonResponse({'data':{'filePath':  path}})
            else:
                return redirect('milk:media_index')
    if format == 'JSON':
        return JsonResponse({'error': 'importError'})
    else:
        return render(request, 'milk/media.html')


@login_required
def pages(request):
    pages = Page.objects.filter().order_by('-created_at')[:10]
    context = {}
    context['pages'] = []
    for page in pages:
        context['pages'].append(Serializer.page(page))
    return render(request, 'milk/pages.html', context)

@login_required
def page_add(request):
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page_id = request.POST.get('page_id', None)
            if page_id is None:
                page = form.save(commit=False)
                page.author = request.user
                page.published = True
            else:
                page = get_object_or_404(Post, pk=page_id)
                page.title = form.cleaned_data['title']
                page.path = form.cleaned_data['path']
                page.body = form.cleaned_data['body']
            if page.path[0] != '/':
                page.path = '/' + page.path
            page.save()
            return redirect('milk:pages')
        else:
            print(f"Failed to create page {form.errors}")
    return render(request, 'milk/pages_add.html')

@login_required
def pages_edit(request, id):
    page = get_object_or_404(Page, pk=id)
    context = {}
    context['page'] = Serializer.page(page)
    return render(request, 'milk/pages_add.html', context)

@login_required
def page(request, id):
    page = get_object_or_404(Page, pk=id)
    context = {}
    context['page'] = Serializer.page(page)
    return render(request, 'milk/page.html', context)

@login_required
def pages_delete(request, id):
    page = get_object_or_404(Page, pk=id)
    page.delete()
    return redirect('milk:pages')
