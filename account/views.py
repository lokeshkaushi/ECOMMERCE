from django.contrib import messages
from rest_framework import status, response
from .serializers import*
from rest_framework.views import APIView
from rest_framework.response import Response
from .emails import*
from rest_framework_simplejwt.tokens import RefreshToken
import random
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated




def get_tokens_for_user(user):

    ''' THIS FUNCTION PROVIDE TOKEN CREATE MANUALLY '''

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class Register(APIView):
    serializer_class = UserSerializer
    def post(self,request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            email=serializer.initial_data.get('email')
            serializer.save()
            user = vendorregistration.objects.get(email = email)
            current_time = timezone.now()
            if user.Otpcreated_at and user.Otpcreated_at > current_time:
                user.otp = random.randint(1000, 9999)
                user.Otpcreated_at = current_time + timedelta(minutes=15)
            else:
                user.otp = random.randint(1000, 9999)
                user.Otpcreated_at = current_time + timedelta(minutes=15)
            user.save()
            send_otp_via_email(serializer.data['email'],user.otp)
            return Response({'id': str(user.id),"data": serializer.data,'otp':str(user.otp),'message': "Register successfully. sent otp on your email please check."},
                             status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from django.contrib import admin, messages

class VerifyOtp(APIView):
    serializer_class = VerifyOtpSerializer
    def post(self,request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            otp = serializer.data['otp']
            user = vendorregistration.objects.filter(email=email).first()
            if not user:
                return Response({'message': "somthing went wrong","data": "invalid email"},
                             status=status.HTTP_400_BAD_REQUEST)
            current_time = timezone.now()
            if otp == user.otp and user.Otpcreated_at and user.Otpcreated_at > current_time:
                if user.otp == otp:
                    user.is_verifide =True
                    user.save()
                    messages.info(request, f"New vendor {user} is registered. Please approve.")
                    # messages.add_message(request, messages.INFO,f"New vendor {user} is registered. Please approve.")
                    return Response({'message': "Account is verifyd you can login account"},status=status.HTTP_201_CREATED)
            return Response({'message': "Invalid Otp please try again","data": "wrong otp"},status=status.HTTP_400_BAD_REQUEST)    
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


class Login(APIView):
    
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        email = serializer.initial_data.get('email')
        password = serializer.initial_data.get('password')
        user = vendorregistration.objects.filter(email=email).first()
        if not user:
            return Response({'message': "The vendor is not registered "}, status=status.HTTP_403_FORBIDDEN)
        if not user.Is_Approved:
            return Response({'message': "The vendor is registered but is awaiting approval"}, status=status.HTTP_403_FORBIDDEN)
        if user.email==email:
            if user.password==password:
                token = get_tokens_for_user(user)
                return Response({'id': str(user.id),'token':token,'message':'login success'},status=status.HTTP_200_OK)
            else:
                return response.Response({'errors':'Email or Password is not valid'}, status=status.HTTP_404_NOT_FOUND)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ResetPasswordSendEmailView(APIView):
    serializer_class = SendPasswordResetEmailSerializer 
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email=serializer.initial_data.get('email')
        user = vendorregistration.objects.get(email=email)
        current_time = timezone.now()
        if user.Otpcreated_at and user.Otpcreated_at > current_time:
            user.otp = random.randint(1000, 9999)
            user.Otpcreated_at = current_time + timedelta(minutes=1)
        else:
            user.otp = random.randint(1000, 9999)
            user.Otpcreated_at = current_time + timedelta(minutes=1)
        user.save()
        send_otp_via_email_reset_password(email,user.otp)
        return Response({'uid': str(user.uid),'otp':str(user.otp),'message':"Otp send successfully"})
            

class SetNewPasswordView(APIView):
    serializer_class = UserPasswordResetSerializar
    def post(self, request, uid):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            otp =serializer.initial_data.get('otp')
            password =serializer.initial_data.get('password')
            password2 =serializer.initial_data.get('password2')
            profile = vendorregistration.objects.get(uid=uid)
            current_time = timezone.now()
            if otp == profile.otp and profile.Otpcreated_at and profile.Otpcreated_at > current_time:
                if otp == profile.otp:
                    if password == password2:
                        profile.password=password
                        profile.save()
                        return Response({'msg': 'Password reset successfully'}, status=status.HTTP_200_OK)
                    else:
                        return Response({'msg': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message':"Invalid Otp please try again"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class vendoreprofile(APIView):

    # permission_classes = [IsAuthenticated]
    serializer_class = VendorProfileSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data,'message':"profile created successfully"},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class vendorartwork(APIView):
    
    serializer_class = VendorArtworkSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data,'message':" Artwork  uploaded successfully"},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class usersdetail(APIView):
    serializer_class = usersSerializer
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':" pantting book successfully"},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self ,request):
        # if id:
        #     item =users.objects.get(id=id)
        #     serializer = usersSerializer(item)
        #     return Response({'data': serializer.data,'message':"this pantting booked"},status=status.HTTP_200_OK)

        usersdata = users.objects.all()
        serializer = usersSerializer(usersdata, many=True)
        return Response({'data': serializer.data},status=status.HTTP_200_OK)



# class Login(APIView):
#     serializer_class = LoginSerializer
#     def post(self,request):
#         serializer = self.serializer_class(data=request.data)
#         email=serializer.initial_data.get('email')
#         print(email)
#         Coins_trader = venderregistration.objects.filter(email=email).first()
#         print(Coins_trader)
#         if not Coins_trader:
#             return response.Response({'message': "No User found with this mobile"},status=status.HTTP_404_NOT_FOUND)

#         if not Coins_trader.Is_Approved:
#             return Response({'message': "Audio Jockey is not approved. Please wait for some time to Get Approved."}, status=status.HTTP_403_FORBIDDEN)

#         user = venderregistration.objects.get(email=email)
#         user.otp = random.randint(1000, 9999)

#         user.save()
#         send_otp_via_email_login(email,user.otp)
#         return Response({'otp':str(user.otp),'message':"Otp send successfully"})
        
# class Otp(APIView):
#     serializer_class = OtpSerializer
#     def post(self,request,uid):
#         serializer = self.serializer_class(data=request.data)
#         otp =serializer.initial_data.get('otp')
#         profile = venderregistration.objects.get(uid=uid)
#         current_time = timezone.now()
#         if otp == profile.otp :
#             if otp == profile.otp:
#                 # refresh = RefreshToken.for_user(profile)
#                 user_serializer = UserSerializer(profile)
#                 return response.Response({'data': str(user_serializer.data),'id':str(profile.id),'message':"Login successfully"})
#             else:
#                 return response.Response({'message':"Invalid Otp please try again"},status=status.HTTP_400_BAD_REQUEST)    
#         else:
#                 return response.Response({'message':"Invalid Otp please try again"},status=status.HTTP_400_BAD_REQUEST)    
