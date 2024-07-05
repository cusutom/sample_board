from django.db import models

# Create your models here.
class ThemesManager(models.Manager):

    def fetch_all_themes(self):
        return self.order_by('id').all()
    

class Themes(models.Model):

    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        'accounts.Users', on_delete=models.CASCADE
    )

    objects = ThemesManager()

    class Meta:
        db_table = 'themes'


class CommentsManager(models.Manager):
    def fetch_by_theme_id(self, theme_id):
        return self.filter(theme_id=theme_id).order_by('id').all()

class Comments(models.Model):
    
    comment = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('accounts.Users', on_delete=models.CASCADE)
    theme = models.ForeignKey('Themes', on_delete=models.CASCADE)
    attach = models.FileField(verbose_name='添付ファイル',upload_to='media/%Y/%m/%d/',blank=True, null=True)

    objects = CommentsManager()

    class Meta:
        db_table = 'comments'

