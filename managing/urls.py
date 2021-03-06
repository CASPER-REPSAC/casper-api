from django.urls import path
from managing.views import *
from activity.member_management import *
from accounts.views import *

urlpatterns = [
    path('', activity_list),
    path('end/', activity_end_list),
    path('<int:pk>', activity_detail),
    path('<int:pk>/', activity_detail),

    
    # UPDATE uri
    path('<int:pk>/chapter/<int:chapterid>/update_chapter', chapter_update),
    path('<int:pk>/chapter/<int:chapterid>/update_chapter/', chapter_update),

    # DELETE uri
    path('<int:pk>/chapter/<int:chapterid>', chapter_detail),
    path('<int:pk>/chapter/<int:chapterid>/', chapter_detail),

    # File
    path('<int:pk>/chapter/<int:chapterid>/upload/<str:filename>/', FileView.as_view()),  #
    #File
    path('<int:pk>/chapter/<int:chapterid>/download/<str:filename>/', getfile),

    # Comment
    path('write_comment/', write_comment),
    path('delete_comment/<int:commentpk>/', delete_comment),

    # Member management
    path('<int:pk>/member/', member),
    path('<int:pk>/out/', out)
]
