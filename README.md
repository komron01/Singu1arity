# Singu/\arity Registration System

Welcome to the Singu/\arity Registration System! This web application allows users to register for the Singu/\arity platform. Users can check the availability of their desired usernames and complete the registration process.

## Features

- User registration with basic information.
- Real-time username availability check using AJAX.
- Responsive design for a seamless user experience on various devices.
- Error handling for a smooth user interaction.

## Getting Started

### Prerequisites

Before you start, ensure you have the following prerequisites:

- Python 3.x
- Flask framework
- PostgreSQL database

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/singu-arity-registration.git
    cd singu-arity-registration
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up the database:

    - Create a PostgreSQL database and update the `DATABASE_CONFIG` in `settings.py` accordingly.

    ```python
    DATABASE_CONFIG = {
        'dbname': 'your_database_name',
        'user': 'your_database_user',
        'password': 'your_database_password',
        'host': 'localhost',
        'port': '5432',
    }
    ```

4. Run the application:

    ```bash
    python app.py
    ```

The application should be running at [http://localhost:5000](http://localhost:5000).

## Usage

1. Open your web browser and navigate to [http://localhost:5000](http://localhost:5000).
2. Explore the registration form, check username availability, and complete the registration process.

## File Structure
├── static/ # Static files (CSS, JS, images)
│ ├── registration.css # Styles for the registration form
│ └── registration.js # JavaScript file for real-time username availability check
├── templates/ # HTML templates
│ ├── error.html # Error page template
│ ├── index.html # Home page template
│ ├── login.html # Login page template
│ ├── navbar.html # Navbar template
│ ├── registration.html # Registration form template
│ └── success.html # Registration success page template
├── app.py # Main application file
├── settings.py # Application settings
├── registration.db # Sample PostgreSQL database file (replace with your actual database)
└── README.md # Project documentation


## Contributing

If you'd like to contribute to this project, please follow our [contribution guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Singu/\arity team for inspiration and guidance.

---

© 2024 Singu/\arity

