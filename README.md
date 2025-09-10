Django REST Framework User Authentication with OTP Verification
This is a Django REST Framework (DRF) project that provides a secure and robust user authentication system. The system includes features for user registration with email-based OTP verification, token-based login, profile management, and secure password reset and logout functionalities.

Features
User Registration: Create a new user account with an email, username, and password.

OTP-based Email Verification: A One-Time Password (OTP) is sent to the user's email upon registration. The user's account is activated only after successful OTP verification.

Token-based Authentication: The system uses JWT (JSON Web Tokens) for secure API authentication.

User Profile Management: Authenticated users can retrieve their profile details.

Password Reset: Users can change their password after logging in.

Secure Logout: A refresh token blacklisting mechanism ensures that logged-out tokens cannot be used for subsequent requests.

Prerequisites
Before you begin, ensure you have the following installed on your machine:

Python (3.8+)

pip (Python package installer)

Django

Django REST Framework

Installation
Follow these steps to set up the project locally.

1. Clone the repository
git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
cd your-repository-name

2. Create a virtual environment
It's highly recommended to use a virtual environment to manage dependencies.

python -m venv venv

3. Activate the virtual environment
On Windows:

.\venv\Scripts\activate

On macOS/Linux:

source venv/bin/activate

4. Install dependencies
Install all required Python packages.

pip install -r requirements.txt

You can create a requirements.txt file with the following contents:

# requirements.txt
Django
djangorestframework
djangorestframework-simplejwt

5. Database Migrations
Apply the database migrations to create the necessary tables, including the custom User model.

python manage.py makemigrations
python manage.py migrate

6. Configure Email Settings
This project requires a backend for sending emails for OTP verification. Add the following to your settings.py file or a separate .env file.

# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'

# A setting for maximum OTP attempts
MAX_OTP_ATTEMPTS = 3

7. Run the development server
python manage.py runserver

The API will now be running on http://127.0.0.1:8000/.

API Endpoints
The API is structured with the following endpoints:

Endpoint

Method

Description

api/register/

POST

Registers a new user and sends an OTP via email.

api/otp/verify/

POST

Verifies the OTP to activate the user's account.

api/otp/resend/

POST

Resends a new OTP to the user's email.

api/login/

POST

Logs in a user and returns JWT tokens.

api/profile/

GET

Retrieves the profile of the authenticated user.

api/password/reset/

POST

Allows an authenticated user to change their password.

api/logout/

POST

Logs out the user by blacklisting the refresh token.

Usage Examples
Here are some examples of how to interact with the API endpoints.

Register a new user
curl -X POST [http://127.0.0.1:8000/api/register/](http://127.0.0.1:8000/api/register/) \
-H "Content-Type: application/json" \
-d '{
    "email": "testuser@example.com",
    "username": "testuser",
    "phone_number": "1234567890",
    "password": "strongpassword123"
}'

Verify OTP
curl -X POST [http://127.0.0.1:8000/api/otp/verify/](http://127.0.0.1:8000/api/otp/verify/) \
-H "Content-Type: application/json" \
-d '{
    "email": "testuser@example.com",
    "otp": "123456"
}'

Log in
curl -X POST [http://127.0.0.1:8000/api/login/](http://127.0.0.1:8000/api/login/) \
-H "Content-Type: application/json" \
-d '{
    "email": "testuser@example.com",
    "password": "strongpassword123"
}'

Get user profile (requires access token in Authorization header)
curl -X GET [http://127.0.0.1:8000/api/profile/](http://127.0.0.1:8000/api/profile/) \
-H "Authorization: Bearer <your_access_token>"

Change password (requires access token)
curl -X POST [http://127.0.0.1:8000/api/password/reset/](http://127.0.0.1:8000/api/password/reset/) \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_access_token>" \
-d '{
    "old_password": "strongpassword123",
    "new_password": "newpassword456",
    "confirm_password": "newpassword456"
}'

Log out (requires refresh token)
curl -X POST [http://127.0.0.1:8000/api/logout/](http://127.0.0.1:8000/api/logout/) \
-H "Content-Type: application/json" \
-d '{
    "refresh_token": "<your_refresh_token>"
}'

This README.md file provides a solid foundation for your project, making it easy for other developers to understand and contribute.
