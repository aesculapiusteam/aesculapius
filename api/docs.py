aesculapius = """
Here you can see all the global variables of aesculapius with the method /current
"""

profiles = """
# Permissions for Profile
*All permissions listed below have to be true in order to give access to the
client*

### IsAuthenticated
- All permissions are allowed if the user is not anonymous (is authenticated)

### IsAdminOrOwnerOrReadOnly
- All read permissions are allowed to any user for any object
- All write permissions are allowed to Admin users for any object
- All write permissions are allowed to any user for objects that are not
    related to system users
- Object write permissions are allowed only to the user that owns that
    profile or employee object for objects **related to/that are** employees


# Profile Serializer
- id (IntegerField)
- **first_name** (CharField) This field is the only required for having a
    profile in the system
- last_name (CharField)
- email (CharField)
- dni (IntegerField)
- birth_date (TimestampField)
- address (CharField)
- phone (CharField)
- cellphone (CharField)
- creation_datetime (TimestampField)
- **employee** (IntegerField) If this profile is from an employee, this is
    the employee id
# Profile SearchFilter and OrderingFilter
- **filter_backends** Filters that the API  will be using
- search_fields
- ordering_fields
- **ordering** Default ordering that the API will use for the view
# Pagination
- **limit** Sets a limit of items in a page, (USAGE: /api/somelist?limit=5 (sets 5 item pages))
- **offset** Goes to the number given of the item (USAGE: /api/somelist?limit=5&offset=10 (sets 5 item pages and goes to the 10th item))
"""

employees = """
# Permissions for Employee
*All permissions listed below have to be true in order to give access to the
client*

### IsAuthenticated
- All permissions are allowed if the user is not anonymous (is authenticated)

### IsAdminOrOwnerOrReadOnly
- All read permissions are allowed to any user for any object
- All write permissions are allowed to Admin users for any object
- All write permissions are allowed to any user for objects that are not
    related to system users
- Object write permissions are allowed only to the user that owns that
    profile or employee object for objects **related to/that are** employees

# Employee Serializer
- id (IntegerField)
- **username** (CharField) Comes from user.username
- **charge** (CharField) Can be either 'doctor' or 'secretary'
- **assist_ed** (ManyToManyField)
    - If employee.charge == 'doctor' assist_ed represents which secretaries
        assist this doctor (secretaries employee id), it can be empty.
    - If employee.charge == 'secretary' assist_ed represents which doctors
        this secretary attends (doctors employee id), it can be empty,
        but shouldn't.
- **profile** (OneToOneField) Is a copy of the profile that corresponds to
    this employee, it can be accessed from /profile/<employee.profile.id>
# Employee SearchFilter and OrderingFilter
- **filter_backends** Filters that the API  will be using
- search_fields
- ordering_fields
- **ordering** Default ordering that the API will use for the view
# Pagination
- **limit** Sets a limit of items in a page, (USAGE: /api/somelist?limit=5 (sets 5 item lists))
- **offset** Goes to the number given of the item (USAGE: /api/somelist?limit=5&offset=10 (sets 5 item lists and goes to the 10th item))
"""

visits = """
# Permissions for Visit
*All permissions listed below have to be true in order to give access to the
client*

### IsAuthenticated
- All permissions are allowed if the user is not anonymous (is authenticated)

### IsDoctor
- All read permissions are allowed to any user for any object
- All write permissions are allowed to admin users for any object
- All write permissions are allowed to doctor users for any non Visit object
- All write permissions are allowed to doctor users only for Visits that the
    same doctor generated.

# Visit Serializer
- **doctor** (IntegerField) Id that represents the doctor of the visit
- **patient** (IntegerField) Id that represents the patient of the visit
- datetime (TimestampField)
- detail (TextField)
"""

drugs = """
# Permissions for Drug
*All permissions listed below have to be true in order to give access to the
client*

### IsAuthenticated
- All permissions are allowed if the user is not anonymous (is authenticated)

# Drug Serializer
- name (CharField)
- description (TextField)
- quantity (IntegerField)
"""

movements = """
Movements Documentation - TODO

This fields are not obligatory, their default values are:

- employee: current employee, you dont have to send it
- detail: ""
- is_donation: false
- movement_type: 0 (0 is for a drug movement, 1 for cash movement)

Example petition

    {
      "profile": 6,
      "items": [
        {
          "detail": "puede o no estar",
          "is_donation": true,
          "drug": 5,
          "drug_quantity": 9
        },
        {
          "movement_type": 1,
          "cash": 23.54
        }
      ]
    }
"""
