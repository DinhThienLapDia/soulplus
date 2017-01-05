from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
import apps.core.api

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('apps.core.urls', namespace='core')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/signup/', apps.core.api.AccountSignup.as_view()),
    url(r'^api/v1/signin/', apps.core.api.AccountSignin.as_view()),
    url(r'^api/v1/facebooksignin/', apps.core.api.FacebookSignin.as_view()),
    url(r'^api/v1/lostpassword/', apps.core.api.LostPassword.as_view()),
    url(r'^api/v1/newpassword/', apps.core.api.LostPassword.as_view()),
    url(r'^api/v1/homeactionlist/', apps.core.api.ListAction.as_view()),
    url(r'^api/v1/notifications/', apps.core.api.GetNotifications.as_view()),
    url(r'^api/v1/getmyaction/', apps.core.api.GetMyAction.as_view()),
    url(r'^api/v1/likeaction/', apps.core.api.LikeAction.as_view()),
    url(r'^api/v1/getlikesaction/', apps.core.api.GetLikesAction.as_view()),
    url(r'^api/v1/comment/', apps.core.api.Comment.as_view()),
    url(r'^api/v1/sendinvitation/', apps.core.api.SendInvitation.as_view()),
    url(r'^api/v1/acceptinvitation/', apps.core.api.AcceptInvitation.as_view()),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)