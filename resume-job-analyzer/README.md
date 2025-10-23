# 🤖 AI-Powered Resume Job Fit Analyzer

A complete end-to-end AI application that analyzes resume-job compatibility using **Django REST API**, **LangChain**, **OpenAI**, and **React**.

## 🎯 Features

✅ **AI-Powered Analysis** - Uses LangChain with OpenAI embeddings and LLM  
✅ **Multiple Input Methods** - Upload files (PDF, DOCX, TXT) or paste text  
✅ **Real-time Processing** - Fast similarity scoring with cosine similarity  
✅ **Detailed Explanations** - AI-generated insights and recommendations  
✅ **Skill Extraction** - Automatically extracts technical skills from resumes  
✅ **Modern UI** - Responsive React frontend with Bootstrap  
✅ **RESTful API** - Clean Django REST Framework backend  
✅ **PostgreSQL Database** - Production-ready data persistence  
✅ **Docker Support** - Complete containerization included

## 🏗️ Architecture

```
[React Frontend] ──HTTP POST──> [Django REST API] ──> [LangChain + OpenAI]
                                        ↓
                                  [PostgreSQL DB]
                                        ↓
                            [Resume Parser + Text Extraction]
```

## 📋 Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **PostgreSQL 12+**
- **OpenAI API Key** (for AI features)

## 🚀 Quick Start Guide

### Step 1: Clone and Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Backend Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Download spaCy model
python -m spacy download en_core_web_sm
```

### Step 3: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and set:
# - SECRET_KEY (generate a secure key)
# - DB_NAME, DB_USER, DB_PASSWORD (PostgreSQL credentials)
# - OPENAI_API_KEY (your OpenAI API key)
```

### Step 4: Setup PostgreSQL Database

```bash
# Start PostgreSQL service
sudo service postgresql start

# Create database
sudo -u postgres psql
```

```sql
CREATE DATABASE resume_analyzer_db;
CREATE USER postgres WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE resume_analyzer_db TO postgres;
\q
```

### Step 5: Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate

# Optional: Create admin user
python manage.py createsuperuser
```

### Step 6: Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### Step 7: Run the Application

**Terminal 1 - Django Backend:**
```bash
python manage.py runserver
```

**Terminal 2 - React Frontend:**
```bash
cd frontend
npm start
```

The application will open at **http://localhost:3000**

## 🐳 Using Docker (Alternative)

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d
```

Access the application at **http://localhost:3000**

## 📍 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/predict_fit/` | Analyze resume-job fit |
| GET | `/api/analysis/` | Get analysis history |
| GET | `/api/analysis/{id}/` | Get specific analysis |
| DELETE | `/api/analysis/{id}/delete/` | Delete analysis |
| POST | `/api/extract_text/` | Extract text from file |
| GET | `/api/supported_formats/` | Supported file formats |
| GET | `/api/health/` | Health check |

## 💡 Usage Examples

### Using the Web Interface

1. **Upload Resume** - Drag & drop or select a file (PDF, DOCX, TXT)
2. **Or Paste Text** - Copy and paste resume content directly
3. **Enter Job Title** - Type the target job position
4. **Add Job Description** - Optional detailed job requirements
5. **Click Analyze** - Get AI-powered compatibility score and insights

### Using the API with cURL

```bash
# Analyze with resume text
curl -X POST http://localhost:8000/api/predict_fit/ \
  -F "resume_text=Software Engineer with 5 years Python experience..." \
  -F "job_title=Senior Python Developer"

# Analyze with file upload
curl -X POST http://localhost:8000/api/predict_fit/ \
  -F "resume_file=@resume.pdf" \
  -F "job_title=Data Scientist"
```

### Using Python

```python
import requests

response = requests.post('http://localhost:8000/api/predict_fit/', data={
    'resume_text': 'Your resume content...',
    'job_title': 'Machine Learning Engineer',
    'job_description': 'Python, TensorFlow, PyTorch required'
})

result = response.json()
print(f"Score: {result['similarity_score']}%")
print(f"Analysis: {result['fit_explanation']}")
```

## 📦 Project Structure

```
resume-job-analyzer/
├── resume_analyzer/          # Django project settings
│   ├── settings.py          # Configuration
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI config
├── api/                      # Django API app
│   ├── models.py            # Database models
│   ├── views.py             # API endpoints
│   ├── serializers.py       # DRF serializers
│   ├── urls.py              # API URLs
│   └── utils.py             # LangChain utilities
├── frontend/                 # React frontend
│   ├── public/              # Static assets
│   ├── src/
│   │   ├── App.js          # Main component
│   │   └── App.css         # Styling
│   └── package.json        # Dependencies
├── requirements.txt          # Python dependencies
├── manage.py                # Django management
├── docker-compose.yml       # Docker config
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=resume_analyzer_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# OpenAI
OPENAI_API_KEY=your_openai_api_key
```

## 🚨 Troubleshooting

### Common Issues

**1. Database Connection Error**
```bash
# Check PostgreSQL is running
sudo service postgresql status

# Test connection
psql -U postgres -d resume_analyzer_db
```

**2. OpenAI API Error**
```bash
# Verify API key is set
echo $OPENAI_API_KEY

# Check key validity
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

**3. CORS Issues**
- Ensure `django-cors-headers` is installed
- Check `CORS_ALLOWED_ORIGINS` in `settings.py`
- Verify React proxy in `package.json`

**4. File Upload Problems**
```bash
# Check media directory exists
mkdir -p media/resumes

# Verify permissions
chmod 755 media/resumes
```

## 🧪 Testing

```bash
# Run Django tests
python manage.py test

# Run specific test
python manage.py test api.tests

# Run React tests
cd frontend
npm test
```

## 🔐 Security Best Practices

1. ✅ Never commit `.env` file or API keys
2. ✅ Use strong SECRET_KEY in production
3. ✅ Set `DEBUG=False` in production
4. ✅ Configure proper CORS origins
5. ✅ Use HTTPS in production
6. ✅ Validate file uploads (type, size)
7. ✅ Use strong database passwords

## 📊 How It Works

### Analysis Process

1. **Input Processing**
   - Accept resume file or text
   - Extract text from PDF/DOCX/TXT
   - Parse job title and description

2. **AI Analysis**
   - Generate embeddings using OpenAI
   - Calculate cosine similarity
   - Extract skills and experience
   - Generate LLM explanation

3. **Results**
   - Similarity score (0-100%)
   - Detailed AI explanation
   - Extracted skills
   - Recommendations

### Technology Stack

**Backend:**
- Django 4.2.7
- Django REST Framework 3.14.0
- LangChain 0.0.336
- OpenAI API 1.3.5
- PostgreSQL
- scikit-learn (TF-IDF fallback)

**Frontend:**
- React 18.2.0
- Bootstrap 5.3.0
- Axios 1.4.0

**AI/ML:**
- OpenAI Embeddings
- LangChain LLM
- Cosine Similarity
- TF-IDF Vectorization

## 🎓 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [React Documentation](https://react.dev/)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- OpenAI for GPT and embedding models
- LangChain for AI framework
- Django and React communities

## 📞 Support

For issues or questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review API documentation

---

**Built with ❤️ using Django, React, and LangChain**

🚀 **Happy Analyzing!**
