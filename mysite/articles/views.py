from django.shortcuts import render, redirect, get_object_or_404
# DVDH
# django가 주는 views에서 쓸 decorators http를 위한 것
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from IPython import embed

# Create your views here.
def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)

def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comment_form = CommentForm()
    # 1은 N을 보장할 수 없기 때문에 querySet(comment_set)
    # 형태로 조회 해야한다.
    comments = article.comment_set.all()
    context = {
        'article': article,
        'comment_form' : comment_form,
        'comments' : comments
    }
    return render(request, 'articles/detail.html', context)

@login_required
def create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form
    }
    return render(request, 'articles/form.html', context)

@login_required
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm(instance=article)
    context = {
        'form': form
    }
    return render(request, 'articles/form.html', context)


@require_POST
def delete(request, article_pk):

    article = get_object_or_404(Article, pk=article_pk)
    # if request.method == "POST":
    article.delete()
    # return redirect('articles:index')
    return redirect('articles:detail', article.pk)

@require_POST
def comment_create(request, article_pk):
    # article = Article.objects.get(pk=article_pk)
    article = get_object_or_404(Article, pk=article_pk)
    # form 태그에서 넘어온 댓글 내용 가져오기
    # comment = request.POST.get('content')
    #댓글 생성 및 저장 
    # comment = Comment(article=article, content=comment)
    # comment.save()

    # if request.method == "POST":
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        # 댓글은 생성하지만 DB에는 반영을 하지 않겠다는 뜻이다.
        comment = comment_form.save(commit=False)
        comment.article = article
        # 또 다른 방법
        # 작성하는 숫자는 article의 pk값
        # comment.article_id = article.pk
        comment.save()
        # 댓글 생성 후 디테일 페이지로 redirect 해준다
        return redirect('articles:detail', article.pk)
    else:
        context = {
            'comment_form' : comment_form,
            'article' : article,
        }
    return redirect('articles:detail', article.pk, context)              

@require_POST
def comment_delete(request, article_pk, comment_pk):
    # comment = Comment.objects.get(pk=comment_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    # if request.method == "POST":
    #     comment.delete()
        # return redirect('articles:detail', article_pk)
    return redirect('articles:detail', article_pk)
