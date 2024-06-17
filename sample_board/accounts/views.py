from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Users
# Create your views here.

#ウェルカム画面表示
def welcome(request):
    return render(
        request, 'accounts/welcome.html'
    )

#ホーム画面表示
def home(request):
    return render(
        request, 'accounts/home.html'
    )

#登録処理
def regist(request):
    regist_form = forms.RegistForm(request.POST or None)
    if regist_form.is_valid():
        try: #例外処理
            regist_form.save()
            return redirect('accounts:home') 
        except ValidationError as e:
            regist_form.add_error('password', e)
    return render(
        request, 'accounts/regist.html',context={ 
            'regist_form': regist_form,
        }
    )

#新規登録処理
def new_regist(request):
    new_regist_form = forms.RegistForm(request.POST or None)
    if new_regist_form.is_valid():
        try: #例外処理
            new_regist_form.save()
            return redirect('accounts:home') 
        except ValidationError as e:
            new_regist_form.add_error('password', e)
    return render(
        request, 'accounts/new_regist.html',context={ 
            'new_regist_form': new_regist_form,
        }
    )

#ログイン処理
def login_user(request):
    login_form = forms.loginForm(request.POST or None)
    if login_form.is_valid(): 
        school_id = login_form.cleaned_data.get('school_id') 
        password = login_form.cleaned_data.get('password')
        user = authenticate(school_id=school_id, password=password) 
        if user: 
            if user.is_active:  #userが認証されている場合
                login(request, user) 
                messages.success(request, f'ログインしました')
                return redirect('accounts:home') 
            else: #user認証されていない場合
                messages.warning(request, 'ユーザーが登録されていません') 
        else: #(学籍番号とパスワードが一致した)userが取得できなかった場合
            messages.warning(request, '学籍番号かパスワードが間違っています')
    
    return render( 
        request, 'accounts/login.html', context={ 
            'login_form': login_form, 
        }
    )

#ログアウト処理
@login_required 
def logout_user(request):  
    logout(request) 
    messages.success(request, 'ログアウトしました') 
    return redirect('accounts:welcome') 

#ユーザー情報更新処理
@login_required
def edit_user(request):
    user_edit_form = forms.UserEditForm(request.POST or None, request.FILES or None, instance=request.user)
    if user_edit_form.is_valid():
        messages.success(request, '更新完了しました')
        user_edit_form.save()
    return render(request, 'accounts/edit.html', context={
        'user_edit_form': user_edit_form,
    })

#アカウント削除処理
@login_required
def delete_user(request, **kwargs):
    user = get_object_or_404(Users, **kwargs)
    delete_user_form = forms.UserDeleteForm(request.POST or None)
    if delete_user_form.is_valid():
        user.delete()
        messages.success(request, 'ユーザーアカウントを削除しました')
        return redirect('accounts:welcome')
    return render(
        request, 'accounts/delete.html', context={
            'delete_user_form': delete_user_form
        }
    )


