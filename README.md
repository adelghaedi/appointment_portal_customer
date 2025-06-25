# Appointment Portal Customer Module for Odoo 17

This is a custom Odoo 17 module that provides a customer-facing portal for appointment scheduling. It integrates seamlessly with the [Appointment Module](https://github.com/adelghaedi/appointment_module) to allow customers to view employees, work fields, and services, book appointments, and ensure time validations.

## 🔧 Features

- **Customer Portal Access**: Customers can log in to a dedicated portal to manage their appointments.
- **Browse Employees and Services**: View available employees, their work fields, and offered services.
- **Appointment Scheduling**: Book appointments with the employee.
- **Time Validations**: Ensures no overlapping appointments and validates booking times based on employee schedules.
- **User-Friendly Interface**: Fully integrated with Odoo's frontend for a smooth customer experience.
- **Secure Access**: Role-based access ensures customers only see relevant data.

## 🧩 Dependencies

- Odoo 17
- Python 3.10+
- [Appointment Module](https://github.com/adelghaedi/appointment_module)
- `portal` (Odoo's customer portal module)
- `website` (Odoo's website module)
- No additional third-party modules required

## 🚀 Installation

1. Ensure the [Appointment Module](https://github.com/adelghaedi/appointment_module) is installed in your Odoo instance.
2. Clone this repository into your Odoo custom addons directory:
   ```bash
   git clone https://github.com/adelghaedi/appointment_portal_customer.git
   ```
3. Update the Odoo apps list:
   - In Odoo, navigate to **Apps** and click **Update Apps List**.
4. Search for `appointment_portal_customer` and install the module.