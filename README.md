# Cosmetic Shop Management System

A web-based management system built with Flask for managing cosmetic shop operations including employees, customers, products, suppliers, orders, and payments.

## Features

- **User Authentication**: Secure login/logout system with password hashing
- **Employee Management**: Add, update, delete, and view employee records
- **Customer Management**: Manage customer information and contact details
- **Product Management**: Track cosmetic products with categories, prices, and expiration dates
- **Supplier Management**: Maintain supplier information and contact details
- **Order Management**: Process and track customer orders with order items
- **Payment Processing**: Record and manage payment transactions
- **Data Export**: Export data to CSV format for reporting
- **Responsive Dashboard**: User-friendly interface for easy navigation

## Technology Stack

- **Backend**: Flask (Python 3.x)
- **Database**: MySQL
- **Frontend**: HTML5, CSS3
- **Security**: Werkzeug password hashing, session management
- **Deployment**: Gunicorn WSGI server (ready for Render/Heroku)

## Database Schema

The system uses the following database tables:

- **Employee**: EmpID, Name, Email, PhoneNo, Position, Salary, JoinDate
- **Customer**: CusID, Name, Email, PhoneNo
- **Product**: ProdID, ProductName, Category, Price, ExpDate
- **Supplier**: SuppID, SuppName, Email, PhoneNo, Address
- **Orders**: OrderID, OrderDate, TotalAmount, CusID (FK)
- **OrderItem**: ItemID, OrderID (FK), ProdID (FK), Quantity, Price
- **Payment**: PaymentID, PaymentMethod, Amount, PaymentDate, OrderID (FK)

## Prerequisites

- Python 3.7 or higher
- MySQL Server 5.7 or higher
- pip (Python package installer)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AnshuNandi/Cosmetic-Shop.git
   cd Cosmetic-Shop
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MySQL database**
   - Create a new MySQL database:
     ```sql
     CREATE DATABASE cosmetic_shop;
     ```

5. **Configure environment variables**
   - Create a `.env` file in the project root:
     ```
     FLASK_SECRET_KEY=your_secret_key_here
     DB_HOST=localhost
     DB_USER=root
     DB_PASSWORD=your_mysql_password
     DB_NAME=cosmetic_shop
     PORT=5000
     ```
   - Generate a secure secret key using:
     ```bash
     python -c 'import secrets; print(secrets.token_hex(16))'
     ```

6. **Initialize the database**
   - The application will automatically create all required tables on first run

## Usage

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Access the application**
   - Open your web browser and navigate to: `http://localhost:5000`

3. **Login credentials** (default credentials - change for production use)
   - **Username**: `admin` | **Password**: `admin`
   - **Username**: `user` | **Password**: `user`
   
   > ⚠️ **Security Note**: These are default credentials for development only. For production deployment, modify the `users` dictionary in `app.py` with secure passwords.

4. **Navigate through the dashboard**
   - Manage Employees
   - Manage Customers
   - Manage Products
   - Manage Suppliers
   - Manage Orders
   - Export Data

## Deployment

The application is configured for deployment on cloud platforms like Render or Heroku:

- `Procfile` is included for Gunicorn WSGI server
- The app binds to `0.0.0.0` and uses the `PORT` environment variable
- Set environment variables on your hosting platform matching the `.env` configuration

## Project Structure

```
Cosmetic-Shop/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── Procfile              # Deployment configuration
├── .gitignore            # Git ignore rules
├── static/
│   └── style.css         # CSS styles
└── templates/
    ├── login.html        # Login page
    ├── dashboard.html    # Main dashboard
    └── manage.html       # CRUD operations page
```

## Security Features

- Password hashing using Werkzeug's security utilities
- Session-based authentication
- Environment variable configuration for sensitive data
- SQL parameterized queries to prevent SQL injection

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source.

## Author

**Anshu Nandi**

## Support

For issues, questions, or contributions, please open an issue in the GitHub repository.
