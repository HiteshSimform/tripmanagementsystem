from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, PermissionManager, PermissionsMixin

# class UserManager(BaseUserManager):
#     def create_user(self, email, username, password=None, role="guest"):
#         allowed_roles= ['guest','participant','viewer']
#         if role not in allowed_roles:
#             raise ValueError(f"Role '{role}' can not be self-assigned.")

#         if not email:
#             raise ValueError("Users must have an email address")
#         email = self.normalize_email(email)
#         user = self.model(email=email, username=username, role=role)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
    
#     def create_superuser(self,email, username, password):
#         user = self.create_user(email=email,username=username, password=password,role="admin")
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, role="guest"):
        # Prevent role hijack but allow flexibility for superusers
        restricted_roles = ['guest', 'participant', 'viewer']
        if role not in restricted_roles:
            raise ValueError(f"Role '{role}' cannot be self-assigned.")

        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        # Directly create user instance without going through role restrictions
        if not email:
            raise ValueError("Superuser must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, role="admin")
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
