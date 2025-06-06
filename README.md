# Undiscriminating Discriminator

## Overview
Undiscriminating Discriminator is a conceptual pilot to explore the technical feasibility of a "least discriminating multi-model approach" to AI in HR skill management. It is currently in the MVP phase and does not have rich features apart from adding the basic conceptual data types via the Django native REST frontend management.

## Features
- Basic conceptual data types management via Django REST framework.
- MVP implementation for testing feasibility.
- Simple and minimalistic design for experimentation.

## Installation
To install the project, follow these steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/undiscriminating_discriminator.git
   ```
2. Navigate to the project directory:
   ```bash
   cd undiscriminating_discriminator
   ```
3. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

## Usage
To run the development server, use the following command:
```bash
python manage.py runserver
```

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push the branch.
4. Submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
