# from django.contrib.auth.decorators import login_required
# from django.shortcuts import redirect, render
# from django.http import HttpResponse

# from users.models import UserRole


# @login_required
# def dashboard(request):
#     if request.user.is_authenticated:
#         if request.user.role == UserRole.STUDENT:
#             return render(request, 'student/dashboard.html')
#         return redirect('/admin/')
#     return redirect('/accounts/login/')
