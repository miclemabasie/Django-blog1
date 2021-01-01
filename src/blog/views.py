from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from . forms import *
from django.core.mail import send_mail
from taggit.models import Tag
import concurrent
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity



def home(request):
    context = {
        "method": request.method
    }
    return render(request, 'home.html', context)

# creating a list view to display all the posts
def list_post(request, tag_slug=None):
    post_list = Post.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = Post.objects.filter(tags__in=[tag])
    paginator = Paginator(post_list, 3) # 3 post in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range
        posts = paginator.page(paginator.num_pages)
    print(paginator)
    print(page)
    print(posts)
    context = {
        'posts': posts,
        'page': page,
        'tag': tag,
    }
    return render(request, 'blog/blog.html', context)


# creating a detail view for each post
def post_detail(request, slug, *args, **kwargs):
    post = get_object_or_404(Post, slug=slug)
    tags = post.tags.all()
    
    # getting similar post with the same tags
    tag_list_ids = post.tags.values_list('id', flat=True)
    similar_post = Post.objects.filter(tags__in=tag_list_ids)
    similar_post = similar_post.exclude(id=post.id)
    similar_post = similar_post.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    # get the list of related comments
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST or None)
        if comment_form.is_valid():
            # create a comment but dont save if yet
            new_comment = comment_form.save(commit=False)
            # assign the current user to the form
            new_comment.post = post
            # save the comment to the database
            new_comment.save()
            print('saved')
        else:
            print(comment_form.errors)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'tags': tags,
        'similar_post': similar_post
    }
    return render(request, 'detail.html', context)


# using class based views
# class PostList(ListView):
#     queryset = Post.published.all()
#     template_name = 'list.html'
#     paginate_by = 3
#     context_object_name = 'posts'


# share post via Email
def share_post(request, id, *args, **kwargs):
    post = get_object_or_404(Post, id=id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST or None)
        if form.is_valid():
            # form passed validation
            data = form.cleaned_data
            # ...send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            name = data['name']
            title = post.title
            subject = f"{name} recommends you read {title}"
            message = f"Read {title} at {post_url} \n {name}\'s comments"
            send_mail(subject, message, 'admin@blog.com', [data['to']])

            sent = True
        else:
            print(form.errors)
    else:
        form = EmailPostForm()
    
    context = {
        'post': post,
        'form': form, 
        'sent': sent
    }

    return render(request, 'share.html', context)


# # search fucntionality:
# def search(request):
    
#     query = None
#     post_list = []
#     if request.method == 'POST'
#         form = SearchForm(request.POST or None)
#         if form.is_valid():
#             query = form.cleaned_data.get('query')
#             post_list = Post.objects.annotate(search=SearchVector('title', 'body'),).filter(search=query)
#             context = {
#             'posts': post_list,
#             'form': form,
#         }
  
#     form = SearchForm()
    
#     context = {
#             'form': form,
#         }
#     return render(request, 'search.html', context)



def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        print(request.GET)

        
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)

            results = Post.published.annotate(similarity=TrigramSimilarity('title', query),).filter(similarity__gt=0.1).order_by('-similarity')
        
    context = {
        'results': results,
        'form': form,
        'query': query,
    }
    
    return render(request, 'search.html', context)
    
    
# The backend part of this project ended on Sunday December 27th 9:00PM