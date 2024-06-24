from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from datetime import datetime
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(
            self,
            school_id,
            class_id,
            first_name,
            last_name,
            first_name_phonetic,
            last_name_phonetic,
            birthday,
            school_grade,
            school_class,
            email,
            club,
            gender,
            status,
            password=None
        ):
        
        user = self.model(
            school_id=school_id,
            class_id=class_id,
            first_name=first_name,
            last_name=last_name,
            first_name_phonetic=first_name_phonetic,
            last_name_phonetic=last_name_phonetic,
            birthday=birthday,
            school_grade=school_grade,
            school_class=school_class,
            email=email,
            club=club,
            gender=gender,
            status=status,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    #スーパーユーザーの入力項目(管理者用)
    def create_superuser(
            self,
            school_id,
            first_name,
            last_name,
            birthday,
            status,
            password=None
        ):

        user = self.model(
            school_id=school_id,
            first_name=first_name,
            last_name=last_name,
            birthday=birthday,
            status=status,
        )

        user.set_password(password)
        user.is_staff = True
        user.is_active = True 
        user.is_superuser = True 
        user.save(using=self._db) 
        return user

#ユーザーモデル(教師、保護者、生徒含む)
class Users(AbstractBaseUser, PermissionsMixin):
    school_id = models.IntegerField(unique=True) #学籍番号
    class_id = models.IntegerField(blank=True, null=True) #出席番号、教師は出席番号をもたないため、必須にはしない。
    first_name = models.CharField(max_length=150) #姓
    last_name = models.CharField(max_length=150) #名
    first_name_phonetic = models.CharField(max_length=150) #姓ふりがな
    last_name_phonetic = models.CharField(max_length=150) #名ふりがな
    birthday = models.DateField() #誕生日
    school_grade = models.PositiveIntegerField(blank=True, null=True) #学年
    school_class = models.PositiveIntegerField(blank=True, null=True) #組
    email = models.EmailField(max_length=150, blank=True, null=True) #学生はメアド持ってない場合があることを想定して必須項目にしない。
    club = models.CharField(max_length=150, blank=True, null=True) #帰宅部想定でnull=True
    is_active = models.BooleanField(default=True) #認証登録は今回は省くためdefault=True
    is_staff = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True) #登録日時
    updated_at = models.DateTimeField(auto_now=True) #更新日時
    GENDER_CHOICES = (
        ('man', 'Man'),
        ('woman', 'Woman'),
    )
    STATUS_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES) #性別
    status = models.CharField(max_length=50, choices=STATUS_CHOICES) #立場

    USERNAME_FIELD = 'school_id'
    REQUIRED_FIELDS = ['first_name', 'last_name','status','birthday'] 

    objects = UserManager() 

    class Meta:
        db_table = 'users' 
    
    def __str__(self):
        return f'{self.school_grade}年{self.school_class}組 : {self.first_name} {self.last_name}' 
    

