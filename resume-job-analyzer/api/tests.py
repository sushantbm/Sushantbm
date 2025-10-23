from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import JobAnalysis, ResumeUpload


class APITestCase(APITestCase):
    def test_health_check(self):
        """Test the health check endpoint"""
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'healthy')

    def test_predict_fit_missing_data(self):
        """Test predict_fit endpoint with missing data"""
        response = self.client.post('/api/predict_fit/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
