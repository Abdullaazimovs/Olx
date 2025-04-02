# OLX-like Platform with FastAPI, Docker, and JWT

This project is an OLX-like platform built using **FastAPI**, containerized with **Docker**, and using **JWT** for secure user authentication. It is designed to allow users to post, search, and manage listings, with a messaging feature for communication between buyers and sellers.

## Features:
- User Authentication with **JWT**
- Posting and managing listings
- Searching and filtering listings
- Real-time messaging
- Admin panel for managing users and listings
- Responsive design for web and mobile

## Technologies:
- **FastAPI**: Backend API framework for high-performance and security.
- **Docker**: To containerize and deploy the application easily.
- **Docker Compose**: For managing multi-container services.
- **NGINX**: As a reverse proxy for handling requests and load balancing.
- **PostgreSQL**: For persistent storage of user data and listings.
- **JWT**: For secure user authentication and session management.

## Services:
This project uses **Docker Compose** to run the following services:
- **app**: FastAPI backend application
- **db**: PostgreSQL database
- **nginx**: Reverse proxy for the FastAPI app

## Setup Instructions:

1. **Clone the repository**:
   ```bash
   git clone git@github.com:yourusername/olx-fastapi-docker.git
   cd olx-fastapi-docker
