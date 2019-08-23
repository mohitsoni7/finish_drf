from django.urls import path
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
	path('list/', views.snippet_list),
	path('list/<int:id>', views.snippet_detail),
	path('list2/', views.snippet_list2),
	path('list2/<int:id>', views.snippet_detail2),
	path('list3/', views.SnippetList.as_view()),
	path('list3/<int:id>', views.SnippetDetail.as_view()),
	path('list4/', views.SnippetList2.as_view()),
	path('list4/<int:pk>', views.SnippetDetail2.as_view()),
	path('list5/', views.SnippetList3.as_view()),
	path('list5/<int:pk>', views.SnippetDetail3.as_view()),
	path('list6/', views.SnippetList4.as_view()),
	path('list6/<int:id>', views.SnippetDetail4.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
