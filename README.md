# House Security System 🏘

The House Security System is a comprehensive solution designed to manage and secure residential buildings. The system
includes functionalities for managing buildings, entrances, and apartments. It also incorporates different user roles
with specific capabilities to ensure efficient and secure management.

## Features

- **User Management**: Create, update, and delete user accounts with specific roles.
- **Building Management**: Add and manage building details, including entrances and apartments.
- **Role-based Access Control**: Ensure that users have access only to the features they need for their role.
- **Logging System**: Comprehensive logging of all user activities and system events to ensure transparency and
  facilitate audits.

## Installation

To clone this project from GitHub, follow these steps:

1. **Open your terminal or command prompt.**
2. **Navigate to the directory where you want to clone the project.**
3. **Run the following commands for cloning project and activating env:**

```shell
git clone https://github.com/MaxymChyncha/house-security-system.git
python -m venv venv
source venv/bin/activate  #for Windows use: venv\Scripts\activate
```

4. **Run next commands for project**:

```shell
pip install -r requirements.txt  # install all dependencies
python manage.py migrate  # transfer all migrations to database
python manage.py create_groups  # create groups for specific roles
python manage.py loaddata database_data.json  # download fixtures to db 
```

### ***Note***: The provided templates are for sample purposes only and are not integrated into the code.
## Documentation

This project use drf-spectacular library for creating simple and comfortable UI.

You can find it using this endpoint `/api/schema/swagger-ui/`