# Tech Mentorship Platform

A web-based platform that connects mentors and mentees in the tech industry. The application allows users to register as mentors or mentees, join chat rooms, manage mentorship sessions, and give feedback.
🚀 Live Demo
Visit the deployed app: [Tech Mentorship Platform](https://tech-mentorship-platform-latest.onrender.com/accounts/register/)

## Features

- User authentication and role management (mentors/mentees)
- Real-time chat system
- Session management
- Feedback and performance tracking
- Automated session reminder emails to mentors and mentees
- Admin dashboard and user analytics

## Technologies

- **Backend:** Django (Python)
- **Database:** SQLite (development)
- **Chat:** Redis (for WebSocket / real-time features)
- **Asynchronous Task Queue**: Celery
- **Task Scheduling (Reminders):**   celery-beat
- **Email Service:** Django’s built-in email backend + smtplib


## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/TechMentorshipPlatform.git
cd TechMentorshipPlatform/tech_mentorship_platform

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver

Visit http://127.0.0.1:8000/ to access the platform locally. You can register as a mentor or mentee, participate in chat sessions, and manage your mentorship profile.

Environment Variables

Create a .env file with the necessary secret keys and Redis configuration. Example:

SECRET_KEY=your-secret-key
```


-📝 License

-This project is open-source and available under the MIT License.



