# Mini Social Network

Mini Social Network is a lightweight social networking platform built using FastAPI. It allows users to create posts, interact with posts by liking or disliking them, and engage with other users within the network.
Features
# 
**User Registration**: Users can register and create an account to join the social network.  
**User Authentication**: Registered users can log in securely to access their accounts.  
**Create Posts**: Users can create posts.  
**Deleting Posts**: Users can delete posts.  
**View Posts**: Users can view posts.  
**Post editing**: Users can edit posts.  
**Like and Dislike Posts**: Users can express their opinion about posts by liking or disliking them.  
#



# Installation  
1. **Create a virtual environment, install dependencies, create a database:**  
     `python -m venv .venv`  
     `pip install -r requirements.txt`  
     `docker-compose -f docker-compose-local.yaml up -d`  

2. **Creating and applying migrations:**  
**Create an alembic base:**  
`alembic init migrations`  
**Change the path to the database in the alembic file (alembic.ini): **  
`sqlalchemy.url = postgresql://postgres:postgres@0.0.0.0:5432/postgres`  
**Import models into env .py**  
`from user.models import Base as BaseUser`  
`from post.models import Base as BasePost`  
`target_metadata = [BaseUser.metadata, BasePost.metadata]`  
**Create the first migration**  
`alembic revision --autogenerate -m "add_user_post"`  
**Apply migrations:**  
`alembic upgrade heads`  

4. **Project start:**  
`uvicorn main:app --port 8000 --reload`  

# Project structure:  
- `.gitignore`: This file specifies the files and directories that should be ignored by Git version control system.
- `README.md`: This is a Markdown file that typically provides information and instructions about the project.
- `base.py`: This file likely contains the base classes or functions that are shared across different parts of the project.
- `docker-compose-local.yaml`: This YAML file is used to define the services, networks, and volumes for local development using Docker Compose.
- `main.py`: This is the main entry point of the application. It could contain the code that initializes and starts the application.
- `post/`: This directory likely represents a module or package related to handling posts.
  - `__init__.py`: This file indicates that the `post` directory is a Python package.
  - `api.py`: This file likely contains the API endpoints and their corresponding handlers for post-related operations.
  - `dals.py`: This file may contain data access layer (DAL) code for interacting with the post-related data storage, such as a database.
  - `models.py`: This file likely defines the data models or database schemas for posts.
  - `schemas.py`: This file may contain the schemas or data validation logic for post-related data.
  - `services.py`: This file likely implements the business logic or services related to post-related operations.
- `requirements.txt`: This file lists the dependencies or packages required for the project, typically in a format that can be installed using pip.
- `security.py`: This file may contain code related to security measures, such as authentication and authorization.
- `session.py`: This file could handle session management, storing and retrieving session information for users.
- `settings.py`: This file likely contains configuration settings for the application, such as database connection details, API keys, or other environment-specific variables.
- `user/`: This directory likely represents a module or package related to handling user-related functionality.
  - `__init__.py`: This file indicates that the `user` directory is a Python package.
  - `api.py`: This file likely contains the API endpoints and their corresponding handlers for user-related operations.
  - `api_login.py`: This file may handle the authentication process and user login functionality.
  - `dals.py`: This file may contain data access layer (DAL) code for interacting with the user-related data storage, such as a database.
  - `hashing.py`: This file could provide functions or utilities for hashing user passwords or other sensitive information.
  - `models.py`: This file likely defines the data models or database schemas for users.
  - `schemas.py`: This file may contain the schemas or data validation logic for user-related data.
  - `services.py`: This file likely implements the business logic or services related to user-related operations.

