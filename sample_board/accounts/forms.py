from django import forms
from .models import Users
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

#登録処理
class RegistForm(forms.ModelForm):
    school_id = forms.IntegerField(label='ユーザーID')
    class_id = forms.IntegerField(label='出席番号')
    first_name = forms.CharField(label='姓')
    last_name = forms.CharField(label='名')
    first_name_phonetic = forms.CharField(label='姓(ふりがな)') 
    last_name_phonetic = forms.CharField(label='名(ふりがな)') 
    birthday = forms.DateField(label='誕生日') 
    school_grade = forms.IntegerField(label='学年', required=False) #教師が学年や組に属さないパターンあるので必須項目にはしない。
    school_class = forms.IntegerField(label='組', required=False) 
    email = forms.EmailField(label='メールアドレス', required=False)#スマホ持たない学生いそう なので必須項目にはしない。
    club = forms.CharField(label='部活動')
    GENDER_CHOICES = (
        ('man', 'Man'),
        ('woman', 'Woman'),
    )
    STATUS_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ) 
    gender = forms.ChoiceField(label='性別', choices=GENDER_CHOICES) 
    status = forms.ChoiceField(label='学校との関係', choices=STATUS_CHOICES) 
    
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput())

    class Meta():
        model = Users
        fields = (
            'school_id',
            'class_id',
            'first_name',
            'last_name',
            'first_name_phonetic',
            'last_name_phonetic',
            'birthday',
            'school_grade',
            'school_class',
            'email',
            'club',
            'gender',
            'status',
            'password',
            )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('パスワードが一致しません')
    
    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()

#ログイン入力欄
class loginForm(forms.Form):
    school_id = forms.CharField(label="ユーザーID")
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput())


#ユーザー情報更新欄
class UserEditForm(forms.ModelForm):
    school_id = forms.IntegerField(label='ユーザーID')
    class_id = forms.IntegerField(label='出席番号')
    first_name = forms.CharField(label='姓')
    last_name = forms.CharField(label='名')
    first_name_phonetic = forms.CharField(label='姓(ふりがな)') 
    last_name_phonetic = forms.CharField(label='名(ふりがな)') 
    school_grade = forms.IntegerField(label='学年', required=False) #教師が学年や組に属さないパターンあるので必須項目にはしない。
    school_class = forms.IntegerField(label='組', required=False) 
    email = forms.EmailField(label='メールアドレス', required=False)#スマホ持たない学生いそう なので必須項目にはしない。
    club = forms.CharField(label='部活動')

    class Meta:
        model = Users
        fields = (
            'school_id',
            'class_id',
            'first_name',
            'last_name',
            'first_name_phonetic',
            'last_name_phonetic',
            'school_grade',
            'school_class',
            'email',
            'club',
            )

class UserDeleteForm(forms.ModelForm):

    class Meta:
        model = Users
        fields = []


class PasswordChangeForm(forms.ModelForm):
    
    old_password = forms.CharField(label='変更前のパスワード', widget=forms.PasswordInput())
    password = forms.CharField(label='新しいパスワード', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='新しいパスワード再入力', widget=forms.PasswordInput())

    class Meta():
        model = Users
        fields = ('old_password','password','confirm_password')
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        old_password = cleaned_data['old_password']
        user = authenticate(password=old_password) 
        if password != confirm_password:
            raise forms.ValidationError('新しいパスワードが異なります')
        if old_password == password:
            raise forms.ValidationError('変更前のパスワードと新しいパスワードは異なるものにしてください')
        if user:
            raise forms.ValidationError('変更前のパスワードが異なります')
            
        
    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user