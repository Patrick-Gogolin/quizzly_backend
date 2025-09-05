🧠 Quizzly Backend

Quizzly is the backend for a quiz generation platform. Users can provide a YouTube video URL, the audio is downloaded and transcribed, and an interactive quiz with 10 multiple-choice questions is automatically generated.
Built with Django and Django REST Framework (DRF), the project uses JWT authentication stored in cookies for secure sessions.

🔧 Features

User registration and login with JWT (stored in secure cookies)

YouTube URL validation

Automatic audio download from YouTube

Audio transcription with OpenAI Whisper

Quiz generation with Google Gemini (10 questions, 4 options each)

Full CRUD functionality for quizzes

 Role-based access: users can only access their own quizzes


🚀 Tech Stack

Python 3.13.1

 Django 5.2

 Django REST Framework (DRF)

 Django SimpleJWT (with cookie support)

 yt-dlp (for audio download)

Whisper (for transcription)

Google Gemini API (for quiz generation)

SQLite (for development)

python-dotenv (for API key management)

📁 Project Structure

quizzly_backend/

├── auth_app/        # Registration, login, JWT cookie handling

├── quiz_app/        # Transcription, quiz generation, CRUD

├── core/            # Settings, routing

├── manage.py

└── db.sqlite3


📦 Installation

1. Clone the repository

        git clone https://github.com/your-username/quizzly_backend.git
        cd quizzly_backend

2. Create and activate a virtual environment

        python -m venv venv
        source venv/bin/activate   # On Windows: venv\Scripts\activate

3. Install dependencies

        pip install -r requirements.txt
   
4. Set up environment variables

   Copy the example file and create your own .env:

       cp .env.example .env


Open .env and fill in your values:

    GEMINI_API_KEY=your_api_key_here


⚠️ .env is ignored by Git and should never be committed.
.env.example remains in the repo as a reference for required variables.

5. Apply migrations

        python manage.py migrate

7. Run the development server

        python manage.py runserver

🔑 API Endpoints


🔐 Authentication

POST /api/register/ – Register a new user

POST /api/login/ – Login, sets access & refresh tokens in cookies

POST /api/refresh/ – Refresh token using cookie

POST /api/logout/ – Logout, deletes cookies

🧠 Quizzes

POST /api/transcribe/ – Create a new quiz from a YouTube video

GET /api/quizzes/ – List all quizzes of the logged-in user

GET /api/quizzes/{id}/ – Retrieve quiz details

PATCH /api/quizzes/{id}/ – Update a quiz

DELETE /api/quizzes/{id}/ – Delete a quiz

⚙️ Requirements
asgiref==3.8.1

Django==5.2.3

djangorestframework==3.16.0

djangorestframework-simplejwt==5.3.1

yt-dlp==2025.x.x

whisper==x.x.x

google-genai==x.x.x

python-dotenv==1.0.1

sqlparse==0.5.3

tzdata==2025.2

NOTES

SQLite is used in development; for production, switch to PostgreSQL or another robust database.

Whisper is currently configured with the tiny model for performance.

Gemini generates strictly valid JSON for quizzes (title, description, 10 questions).

JWT tokens are stored in cookies (HttpOnly, Secure, SameSite=Lax) for safer authentication.

📨 CONTACT

For questions, issues, or contributions, feel free to open an issue or contact the maintainer.

📄 LICENSE

This project is licensed under the MIT License. See the LICENSE file for details.
