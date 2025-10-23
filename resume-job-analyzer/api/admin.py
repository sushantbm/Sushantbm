from django.contrib import admin
from .models import JobAnalysis, ResumeUpload, AnalysisHistory


@admin.register(JobAnalysis)
class JobAnalysisAdmin(admin.ModelAdmin):
    list_display = ['id', 'job_title', 'similarity_score', 'created_at', 'user']
    list_filter = ['created_at', 'embedding_model']
    search_fields = ['job_title', 'resume_text']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(ResumeUpload)
class ResumeUploadAdmin(admin.ModelAdmin):
    list_display = ['id', 'original_filename', 'file_type', 'file_size_mb', 'extraction_status', 'uploaded_at']
    list_filter = ['file_type', 'extraction_status', 'uploaded_at']
    search_fields = ['original_filename', 'extracted_text']
    readonly_fields = ['uploaded_at', 'file_size_mb']


@admin.register(AnalysisHistory)
class AnalysisHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'job_analysis', 'status', 'processing_time', 'created_at']
    list_filter = ['status', 'created_at']
    readonly_fields = ['created_at']
