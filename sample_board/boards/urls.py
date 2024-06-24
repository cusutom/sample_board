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
    path('post_comments/<int:theme_id>', views.post_comments, name='post_comments'),
    path('edit_comment/<int:id>', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:id>', views.delete_comment, name='delete_comment'),
    path('download/<int:id>', views.download, name='download'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)