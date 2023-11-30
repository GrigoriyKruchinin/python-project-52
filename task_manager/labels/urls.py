from django.urls import path
from task_manager.labels.views import (
    LabelsListView, LabelCreateView, LabelUpdateView, LabelDeleteView
)


urlpatterns = [
    path('', LabelsListView.as_view(), name='labels'),
    path('create/', LabelCreateView.as_view(), name='label_create'),
    path('update/', LabelUpdateView.as_view(), name='label_update'),
    path('delete/', LabelDeleteView.as_view(), name='label_delete'),
]
