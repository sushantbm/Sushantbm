from django.db import models
from django.contrib.auth.models import User


class JobAnalysis(models.Model):
    """Model to store resume-job fit analysis results"""

    # Job and resume information
    job_title = models.CharField(max_length=255)
    job_description = models.TextField(blank=True, null=True)
    resume_text = models.TextField()
    resume_file_name = models.CharField(max_length=255, blank=True, null=True)

    # Analysis results
    similarity_score = models.FloatField()
    fit_explanation = models.TextField()

    # Extracted information
    extracted_skills = models.JSONField(default=list, blank=True)
    extracted_experience = models.JSONField(default=dict, blank=True)
    extracted_education = models.JSONField(default=list, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # Analysis configuration
    embedding_model = models.CharField(max_length=100, default='openai')
    analysis_version = models.CharField(max_length=20, default='1.0')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['job_title']),
            models.Index(fields=['created_at']),
            models.Index(fields=['similarity_score']),
        ]

    def __str__(self):
        return f"Analysis: {self.job_title} - {self.similarity_score:.1f}%"

    @property
    def similarity_percentage(self):
        """Return similarity score as percentage"""
        return round(self.similarity_score, 1)


class ResumeUpload(models.Model):
    """Model to track uploaded resume files"""

    FILE_TYPES = [
        ('pdf', 'PDF'),
        ('doc', 'DOC'),
        ('docx', 'DOCX'),
        ('txt', 'TXT'),
    ]

    file = models.FileField(upload_to='resumes/')
    original_filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    file_size = models.PositiveIntegerField()  # in bytes

    # Extracted content
    extracted_text = models.TextField(blank=True)
    extraction_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    extraction_error = models.TextField(blank=True, null=True)

    # Metadata
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Resume: {self.original_filename}"

    @property
    def file_size_mb(self):
        """Return file size in MB"""
        return round(self.file_size / (1024 * 1024), 2)


class AnalysisHistory(models.Model):
    """Model to track analysis history and performance metrics"""

    job_analysis = models.ForeignKey(JobAnalysis, on_delete=models.CASCADE, related_name='history')

    # Performance metrics
    processing_time = models.FloatField()  # in seconds
    embedding_time = models.FloatField(null=True, blank=True)  # in seconds
    llm_response_time = models.FloatField(null=True, blank=True)  # in seconds

    # Technical details
    tokens_used = models.PositiveIntegerField(null=True, blank=True)
    embedding_dimensions = models.PositiveIntegerField(null=True, blank=True)

    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('initiated', 'Initiated'),
            ('embedding', 'Generating Embeddings'),
            ('analyzing', 'Analyzing Fit'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='initiated'
    )

    error_message = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Analysis histories"

    def __str__(self):
        return f"History: {self.job_analysis} - {self.status}"
