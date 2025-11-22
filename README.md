# Smart ATS - Resume Optimizer

🎯 AI-Powered Resume Analysis & Optimization System

## Features

- **ATS Score Analysis** - Get detailed compatibility scores
- **Keyword Matching** - Identify matching and missing keywords
- **Bullet Point Rewriting** - AI-powered improvements
- **Professional Summary** - Generate compelling summaries
- **Grammar Check** - Detect and fix errors
- **Format Fixes** - ATS-compatible formatting tips
- **Skills Gap Analysis** - Identify missing skills
- **PDF Export** - Download optimized resume

## Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **Groq AI** - Llama 3.3 70B model for intelligent analysis
- **PyPDF2 & python-docx** - Document processing

### Frontend
- **React.js** - Modern UI framework
- **Vite** - Fast build tool
- **Axios** - HTTP client

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- Groq API Key ([Get one free](https://console.groq.com/))

### Backend Setup

```powershell
# Clone repository
git clone https://github.com/krishnab0841/Application_Tracking_System.git
cd Application_Tracking_System

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
# Create .env file and add:
GROQ_API_KEY=your_groq_api_key_here
```

### Frontend Setup

```powershell
cd frontend
npm install
```

## Running the Application

### Start Backend (Terminal 1)
```powershell
uvicorn backend:app --reload --port 8000
```

### Start Frontend (Terminal 2)
```powershell
cd frontend
npm run dev
```

### Access Application
Open browser: `http://localhost:5173`

## Usage

1. **Upload Resume** - Select PDF or DOCX file
2. **Paste Job Description** - Copy job posting
3. **Click Check ATS Score** - Get overall analysis
4. **Use Tools** - Click any feature button for specific improvements
5. **Export** - Download optimized resume

## API Endpoints

- `POST /analyze` - Main analysis endpoint
  - Actions: `check_score`, `keyword_match`, `rewrite_bullets`, `summarize`, `grammar_check`, `format_fix`, `add_skills`, `export_pdf`
- `GET /` - Health check
- `GET /health` - Detailed health status

## Project Structure

```
Application_Tracking_System/
├── backend.py           # FastAPI backend
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not in repo)
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── components/     # UI components
│   │   └── index.css       # Styles
│   └── package.json     # Node dependencies
└── README.md
```

## Dependencies

### Backend
- fastapi
- uvicorn
- groq
- python-dotenv
- PyPDF2
- python-docx
- fpdf2
- python-multipart

### Frontend
- react
- axios
- lucide-react
- vite

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

MIT License

## Author

**Krishna Bulbule**
- GitHub: [@krishnab0841](https://github.com/krishnab0841)

## Acknowledgments

- Powered by [Groq](https://groq.com/) AI
- Built with [FastAPI](https://fastapi.tiangolo.com/) & [React](https://react.dev/)

---

⭐ Star this repo if you find it helpful!
