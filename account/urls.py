from django.urls import path
from account.views import*
from . import views
urlpatterns = [
    # path("index",views.index ,name="index"),
    path("register", Register.as_view(),name="register/"),
    path("login", Login.as_view(),name="Login/"),
    path("otp", VerifyOtp.as_view()),
    path('SendPasswordResetEmail/',ResetPasswordSendEmailView.as_view(), name='sendpasswordresetemail'),
    path('reset-pasword/<uid>',SetNewPasswordView.as_view(),name='reset-password'),
    path("profile", vendoreprofile.as_view(),name="profile"),
    path("artwork", vendorartwork.as_view(),name="artwork"),
    path("userdata", usersdetail.as_view(),name="usersdetail"),
]
