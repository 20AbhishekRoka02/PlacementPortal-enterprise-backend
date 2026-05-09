# from allauth.account.forms import SignupForm
# from django import forms

# from users.models import UserRole


# class StudentSignupForm(SignupForm):

#     def save(self, request):
#         user = super().save(request)

#         user.role = UserRole.STUDENT
#         user.save()

#         return user