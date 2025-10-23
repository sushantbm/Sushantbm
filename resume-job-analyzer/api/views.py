import logging
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
import time

from .models import JobAnalysis, ResumeUpload, AnalysisHistory
from .serializers import JobAnalysisSerializer
from .utils import JobFitAnalyzer, ResumeParser

logger = logging.getLogger(__name__)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def predict_fit(request):
    """Main endpoint for resume-job fit prediction"""
    try:
        resume_text = request.data.get('resume_text', '')
        job_title = request.data.get('job_title', '')
        job_description = request.data.get('job_description', '')
        resume_file = request.FILES.get('resume_file')

        if not job_title:
            return Response({'error': 'Job title is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not resume_text and not resume_file:
            return Response({'error': 'Either resume text or file is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Extract text from file if provided
        if resume_file and not resume_text:
            try:
                parser = ResumeParser()
                file_extension = resume_file.name.split('.')[-1].lower()
                resume_text = parser.extract_text_from_file(resume_file, file_extension)

                ResumeUpload.objects.create(
                    file=resume_file,
                    original_filename=resume_file.name,
                    file_type=file_extension,
                    file_size=resume_file.size,
                    extracted_text=resume_text,
                    extraction_status='completed'
                )
            except Exception as e:
                logger.error(f"File processing error: {str(e)}")
                return Response({'error': f'Error processing file: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        # Initialize analyzer
        openai_api_key = getattr(settings, 'OPENAI_API_KEY', None)
        analyzer = JobFitAnalyzer(openai_api_key=openai_api_key)

        # Perform analysis
        try:
            analysis_result = analyzer.analyze_resume_job_fit(
                resume_text=resume_text,
                job_title=job_title,
                job_description=job_description
            )

            # Save analysis to database
            job_analysis = JobAnalysis.objects.create(
                job_title=job_title,
                job_description=job_description,
                resume_text=resume_text[:5000],
                resume_file_name=resume_file.name if resume_file else None,
                similarity_score=analysis_result['similarity_score'],
                fit_explanation=analysis_result['fit_explanation'],
                extracted_skills=analysis_result['extracted_skills'],
                extracted_experience=analysis_result['experience'],
                embedding_model=analysis_result['analysis_method']
            )

            AnalysisHistory.objects.create(
                job_analysis=job_analysis,
                processing_time=analysis_result['processing_time'],
                status='completed'
            )

            response_data = {
                'id': job_analysis.id,
                'similarity_score': analysis_result['similarity_score'],
                'fit_explanation': analysis_result['fit_explanation'],
                'extracted_skills': analysis_result['extracted_skills'],
                'contact_info': analysis_result['contact_info'],
                'experience': analysis_result['experience'],
                'processing_time': analysis_result['processing_time'],
                'analysis_method': analysis_result['analysis_method'],
                'created_at': job_analysis.created_at.isoformat()
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            return Response({'error': f'Analysis failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_analysis_history(request):
    """Get analysis history"""
    try:
        analyses = JobAnalysis.objects.all()[:50]
        serializer = JobAnalysisSerializer(analyses, many=True)
        return Response({'analyses': serializer.data, 'count': analyses.count()}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching history: {str(e)}")
        return Response({'error': 'Could not fetch analysis history'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_analysis_detail(request, analysis_id):
    """Get specific analysis detail"""
    try:
        analysis = JobAnalysis.objects.get(id=analysis_id)
        serializer = JobAnalysisSerializer(analysis)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except JobAnalysis.DoesNotExist:
        return Response({'error': 'Analysis not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_analysis(request, analysis_id):
    """Delete specific analysis"""
    try:
        analysis = JobAnalysis.objects.get(id=analysis_id)
        analysis.delete()
        return Response({'message': 'Analysis deleted successfully'}, status=status.HTTP_200_OK)
    except JobAnalysis.DoesNotExist:
        return Response({'error': 'Analysis not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({'status': 'healthy', 'message': 'Resume Analyzer API is running', 'version': '1.0.0'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def extract_resume_text(request):
    """Extract text from uploaded resume file"""
    try:
        resume_file = request.FILES.get('resume_file')
        if not resume_file:
            return Response({'error': 'Resume file is required'}, status=status.HTTP_400_BAD_REQUEST)

        parser = ResumeParser()
        file_extension = resume_file.name.split('.')[-1].lower()
        extracted_text = parser.extract_text_from_file(resume_file, file_extension)

        return Response({'extracted_text': extracted_text, 'file_info': {
            'filename': resume_file.name, 'size': resume_file.size, 'type': file_extension
        }}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Text extraction error: {str(e)}")
        return Response({'error': f'Could not extract text: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_supported_formats(request):
    """Get list of supported file formats"""
    parser = ResumeParser()
    return Response({'supported_formats': parser.supported_formats, 'max_file_size': '10MB'}, status=status.HTTP_200_OK)
