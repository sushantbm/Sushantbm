from django.urls import path
from . import views

urlpatterns = [
    # Main prediction endpoint
    path('predict_fit/', views.predict_fit, name='predict_fit'),

    # Analysis management
    path('analysis/', views.get_analysis_history, name='analysis_history'),
    path('analysis/<int:analysis_id>/', views.get_analysis_detail, name='analysis_detail'),
    path('analysis/<int:analysis_id>/delete/', views.delete_analysis, name='delete_analysis'),

    # File operations
    path('extract_text/', views.extract_resume_text, name='extract_text'),
    path('supported_formats/', views.get_supported_formats, name='supported_formats'),

    # Health check
    path('health/', views.health_check, name='health_check'),
]
