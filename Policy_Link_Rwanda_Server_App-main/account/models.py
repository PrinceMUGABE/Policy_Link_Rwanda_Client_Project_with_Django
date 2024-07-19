from django.db import models


class User(models.Model):
    # Define choices for user roles
    USER_ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )

    firstname = models.CharField(max_length=100, null=True)
    lastname = models.CharField(max_length=100, null=True)
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=100)  # Saving only hashed password
    role = models.CharField(max_length=10, choices=USER_ROLE_CHOICES, default='user')
    last_login = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username


class Institute(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)


class Department(models.Model):
    name = models.CharField(max_length=100)
    # Assuming institutionId is a foreign key to Institute model
    institutionId = models.ForeignKey('Institute', on_delete=models.CASCADE)


class Policy(models.Model):
    name = models.CharField(max_length=100)
    # Assuming departmentId is a foreign key to Department model
    departmentId = models.ForeignKey('Department', on_delete=models.CASCADE)
    # institute = models.ForeignKey('Institute', on_delete=models.CASCADE, null=True)
    description = models.TextField()

    def get_department_and_institute(self):
        # Retrieve corresponding department and institute for the policy
        department = self.departmentId
        institute = department.institutionId
        return department, institute
