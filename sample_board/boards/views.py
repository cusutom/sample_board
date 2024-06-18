from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from .models import Themes, Comments
from django.http import Http404
from django.contrib import messages
from django.core.cache import cache
from django.core.paginator import Paginator
# Create your views here.

#掲示板作成
def create_theme(request):
    create_theme_form = forms.CreateThemeForm(request.POST or None)
    if create_theme_form.is_valid(): #formsで作成する必要あり
        create_theme_form.instance.user = request.user
        create_theme_form.save()
        messages.success(request, '掲示板を作成しました')
        return redirect('boards:list_themes')
    
    return render(
        request, 'boards/create_theme.html', context={
            'create_theme_form': create_theme_form
        }
    )

def list_themes(request):
    themes = Themes.objects.fetch_all_themes() #なんやこれ
    return render(
        request, 'boards/list_themes.html', context={
            'themes': themes
        }
    )

#掲示板更新
def edit_theme(request, id):
    theme = get_object_or_404(Themes, id=id)
    if theme.user.id != request.user.id:
        raise Http404
    edit_theme_form = forms.CreateThemeForm(request.POST or None, instance=theme)
    if edit_theme_form.is_valid():
        edit_theme_form.save()
        messages.success(request, '掲示板を更新しました')
        return redirect('boards:list_themes')
    return render(
        request, 'boards/edit_theme.html', context={
            'edit_theme_form': edit_theme_form,
            'id': id,
        }
    )

#掲示板削除
def delete_theme(request, id):
    theme = get_object_or_404(Themes, id=id)
    if theme.user.id !=request.user.id:
        raise Http404
    delete_theme_form = forms.DeleteThemeForm(request.POST or None)
    if delete_theme_form.is_valid():
        theme.delete()
        messages.success(request, '掲示板を削除しました')
        return redirect('boards:list_themes')
    return render(
        request, 'boards/delete_theme.html', context={
            'delete_theme_form': delete_theme_form
        }
    )

#コメント投稿
def post_comments(request, theme_id):
    post_comment_form = forms.PostCommentForm(request.POST or None,)
    theme = get_object_or_404(Themes, id=theme_id)
    comments = Comments.objects.fetch_by_theme_id(theme_id)
    if post_comment_form.is_valid():
        if not request.user.is_authenticated:
            raise Http404
        post_comment_form.instance.theme = theme
        post_comment_form.instance.user = request.user
        post_comment_form.instance.attach = request.FILES['attach']
        post_comment_form.save()
        return redirect('boards:post_comments', theme_id=theme_id)
    return render(
        request, 'boards/post_comments.html', context={
            'post_comment_form': post_comment_form,
            'theme': theme,
            'comments': comments,
        }
    )

#検索機能
def search_themes(request): 
        queryset = Themes.objects.fetch_all_themes() #querysetにThemesモデルのデータを全て格納
        queryset = queryset.order_by('-pk') #降順に整理
        query = request.GET.get('query') #query(検索に入力された言葉)を取得

        if query: #もし検索ワードあれば
            queryset = queryset.filter(title__icontains=query) #タイトルを検索ワードでフィルターかけてthemesデータを抽出
        # search_themesに検索ワードと抽出したthemesを渡す。
        return render(
        request, 'boards/search_themes.html', context={
            'query': query,
            'queryset': queryset,            
            }
        )
        
    

