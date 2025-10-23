from rest_framework import serializers
from .models import JobAnalysis, ResumeUpload, AnalysisHistory


class JobAnalysisSerializer(serializers.ModelSerializer):
    """Serializer for JobAnalysis model"""

    similarity_percentage = serializers.ReadOnlyField()

    class Meta:
        model = JobAnalysis
        fields = [
            'id', 'job_title', 'job_description', 'resume_text', 'resume_file_name',
            'similarity_score', 'similarity_percentage', 'fit_explanation',
            'extracted_skills', 'extracted_experience', 'extracted_education',
            'created_at', 'updated_at', 'embedding_model', 'analysis_version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'similarity_percentage']


class ResumeUploadSerializer(serializers.ModelSerializer):
    """Serializer for ResumeUpload model"""

    file_size_mb = serializers.ReadOnlyField()

    class Meta:
        model = ResumeUpload
        fields = [
            'id', 'file', 'original_filename', 'file_type', 'file_size', 'file_size_mb',
            'extracted_text', 'extraction_status', 'extraction_error', 'uploaded_at'
        ]
        read_only_fields = ['id', 'uploaded_at', 'file_size_mb']


class AnalysisHistorySerializer(serializers.ModelSerializer):
    """Serializer for AnalysisHistory model"""

    class Meta:
        model = AnalysisHistory
        fields = [
            'id', 'job_analysis', 'processing_time', 'embedding_time', 'llm_response_time',
            'tokens_used', 'embedding_dimensions', 'status', 'error_message', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
