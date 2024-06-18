from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'boards'


urlpatterns = [
    path('create_theme', views.create_theme, name='create_theme'),
    path('list_themes', views.list_themes, name='list_themes'),
    path('search_themes', views.search_themes, name='search_themes'),
    path('edit_theme/<int:id>', views.edit_theme, name='edit_theme'),
    path('delete_theme/<int:id>', views.delete_theme, name='delete_theme'),
    path('post_comments/<int:theme_id>', views.post_comments, name='post_comments'), #<int:theme_id>でタイトルごとにidを振ってページを自動で作成し、接続することができるようになる。
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)