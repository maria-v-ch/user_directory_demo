# User Directory Demo

User Directory Demo is a web application for managing a list of users. The application implements functionality for creating, editing, deleting, and viewing users. It also provides user registration and authorization, access rights management, deployment using Docker, web server setup, database integration, and security features.

## Live Demo

You can try out the User Directory Demo at: [https://paragoni.space](https://paragoni.space)

Feel free to explore the features and functionality of the application on this live demo site.

## Features

- User registration and authentication
- User profile management (create, read, update, delete)
- Role-based access control
- RESTful API with JWT authentication
- Swagger/OpenAPI documentation
- Prometheus monitoring integration
- Grafana dashboard for visualizing metrics
- Docker containerization for easy deployment
- Nginx as a reverse proxy
- PostgreSQL database
- Continuous Integration and Deployment with GitHub Actions
- Dynamic color palette for a unique visual experience

## Technologies Used

- Python 3.9
- Django 5.1.2
- Django Rest Framework
- Simple JWT for authentication
- drf-yasg for API documentation
- Prometheus for monitoring
- Grafana for metrics visualization
- Docker and Docker Compose
- Nginx
- PostgreSQL 13
- Gunicorn as the WSGI HTTP Server
- GitHub Actions for CI/CD
- JavaScript for dynamic styling

## Project Architecture

This project follows a standard Django MVT (Model-View-Template) architecture with the following enhancements:

- Uses Django's built-in ORM for database operations
- Implements RESTful API using Django Rest Framework
- Utilizes class-based views for better code organization
- Employs custom user model for extended user attributes
- Integrates Prometheus for application monitoring
- Uses Docker for containerization and easy deployment
- Implements CI/CD pipeline using GitHub Actions

## Dynamic Color Palette

One of the unique features of this application is its constantly changing color palette. Each time a user visits the site or navigates between pages, the color scheme of various elements is dynamically updated. This creates a fresh and engaging visual experience for users, making each interaction with the application unique.

The color changes are implemented using JavaScript, which assigns random colors from a predefined palette to different elements on the page. This feature demonstrates the application's modern, interactive design approach.

## Installation and Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/user-directory-demo.git
   cd user-directory-demo
   ```

2. Copy the `.env.sample` file to `.env` and update the environment variables:
   ```
   cp .env.sample .env
   ```

3. Build and run the Docker containers:
   ```
   docker-compose up --build
   ```

4. The application should now be running at `http://localhost:8080`

## Running Tests

To run the tests, use the following command:

```
docker-compose run web python manage.py test
```

## API Documentation

API documentation is available at `/swagger/` and `/redoc/` endpoints when the server is running.

## Monitoring

- Prometheus is available at `http://localhost:9093`
- Grafana is available at `http://localhost:3000`

## Continuous Integration and Deployment

This project uses GitHub Actions for CI/CD. The workflow includes:

- Automated testing on push and pull requests
- Building and pushing Docker images to a registry
- Deploying to the production environment on successful merges to the main branch

You can view the CI/CD configuration in the `.github/workflows` directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
