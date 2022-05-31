from rest_framework import routers

from django.urls import include, path

from .views import ReviewViewSet, CommentViewSet

app_name = 'apiv1'

router = routers.DefaultRouter()
router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
