from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.crypto import get_random_string
import plotly
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer
import random
import string


@api_view(['GET'])
def index(request):
    return Response({"message": "Welcome to the accounts API"})


@api_view(['POST'])
# @permission_classes([AllowAny])
def signup(request):
    data = request.data
    first_name = data.get('firstname')
    last_name = data.get('lastname')
    email = data.get('email')
    phone = data.get('phone')
    username = data.get('username')

    # Check if email is provided and not empty
    if not email or not email.strip():
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if email already exists in the database
    if CustomUser.objects.filter(email=email).exists():
        return Response({'error': 'Email is already registered'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if phone number is provided and valid
    if not phone or not phone.strip():
        return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
    if len(phone) != 10 or not phone.isdigit():
        return Response({'error': 'Phone number must be 10 digits'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if phone number prefix is valid
    valid_prefixes = ['078', '072', '073', '079']
    if not phone.startswith(tuple(valid_prefixes)):
        return Response({'error': 'The phone number must be from Rwandan Society'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if phone number already exists in the database
    if CustomUser.objects.filter(phone=phone).exists():
        return Response({'error': 'Phone number is already registered'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if username is provided and not empty
    if not username or not username.strip():
        return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if username already exists in the database
    if CustomUser.objects.filter(username=username).exists():
        return Response({'error': 'Username is already taken'}, status=status.HTTP_400_BAD_REQUEST)

    # Generate a random password
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    # Store data in session instead of saving to the database
    request.session['first_name'] = first_name
    request.session['last_name'] = last_name
    request.session['email'] = email
    request.session['phone'] = phone
    request.session['username'] = username
    request.session['password'] = password

    # Send email with account details
    subject = 'Your Account Details'
    message = f'Hello {first_name},\n\nThank you for signing up with us. Here are your account details:\n\nUsername: {username}\nPassword: {password}\n\nPlease verify your password using these credentials.'
    from_email = 'Policy-Link-Rwanda'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

    return Response({'message': 'User data stored. Please check your email for the password.'},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
# @permission_classes([AllowAny])
def verify_password(request):
    entered_password = request.data.get('password')
    actual_password = request.session.get('password')

    if entered_password == actual_password:
        user_data = {
            'first_name': request.session.get('first_name'),
            'last_name': request.session.get('last_name'),
            'email': request.session.get('email'),
            'phone': request.session.get('phone'),
            'username': request.session.get('username'),
            'password': make_password(request.session.get('password'))
        }

        user = CustomUser.objects.create(**user_data)

        # Clear session
        for key in ['first_name', 'last_name', 'email', 'phone', 'username', 'password']:
            if key in request.session:
                del request.session[key]

        return Response({'message': 'Account created successfully. You can now login.'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Invalid password. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
# @permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user = CustomUser.objects.get(username=username)
        if not check_password(password, user.password):
            return Response({'error': 'Invalid password.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Generate OTP
            otp = get_random_string(2, string.ascii_letters) + get_random_string(3, string.digits)
            # Store OTP and username in session with 1 minute expiration
            request.session['otp'] = otp
            request.session['otp_expiry'] = (timezone.now() + timezone.timedelta(minutes=1)).isoformat()
            request.session['username'] = username  # Store username in session

            # Send OTP to user's email
            subject = 'Your OTP Code'
            message = f'Hello {user.username},\n\nYour OTP code is: {otp}\n\nPlease use this to complete your login.'
            from_email = 'Policy-Link-Rwanda'
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)

            return Response({'message': 'OTP sent to your email. Please verify.'}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'error': 'Invalid username.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
# @permission_classes([AllowAny])
def login_otp_verification(request):
    entered_otp = request.data.get('otp')
    actual_otp = request.session.get('otp')
    otp_expiry = request.session.get('otp_expiry')

    # Check if OTP has expired
    if timezone.now() > timezone.datetime.fromisoformat(otp_expiry):
        return Response({'error': 'OTP has expired. Please login again.'}, status=status.HTTP_400_BAD_REQUEST)

    # Verify OTP
    if entered_otp == actual_otp:
        username = request.session.get('username')
        user = CustomUser.objects.get(username=username)

        # Clear OTP and username from session
        for key in ['otp', 'otp_expiry', 'username']:
            if key in request.session:
                del request.session[key]

        # Redirect based on user role
        if user.role == 'admin':
            return redirect('admin_dashboard')
        else:
            return redirect('user_dashboard')
    else:
        return Response({'error': 'Invalid OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def user_dashboard(request):
    return Response({"message": "Welcome to the user dashboard"})


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def admin_dashboard(request):
    return Response({"message": "Welcome to the admin dashboard"})


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def view_all_users(request):
    users = CustomUser.objects.all()
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
# @permission_classes([IsAuthenticated])
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    data = request.data

    serializer = CustomUserSerializer(user, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
        user.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)




'''
    Reports about users
'''


from django.http import HttpResponse, JsonResponse
from .models import CustomUser
from django.db.models import Count

# Total number of users
@api_view(['GET'])
def total_users(request):
    total_users = CustomUser.objects.count()
    return JsonResponse({'total_users': total_users})

# Distribution of users by role
@api_view(['GET'])
def users_distribution(request):
    distribution = CustomUser.objects.values('role').annotate(count=Count('role'))
    return JsonResponse({'users_distribution': list(distribution)})

# List of all users with details
@api_view(['GET'])
def all_users(request):
    users = CustomUser.objects.all()
    user_data = [{'username': user.username, 'email': user.email, 'role': user.role} for user in users]
    return JsonResponse({'users': user_data})





# views.py

import json
from django.http import JsonResponse
import plotly.graph_objects as go

def user_growth_over_years(request):
    # Retrieve user growth data from the database or any other data source
    years = [2020, 2021, 2022, 2023, 2024]
    user_counts = [100, 150, 200, 250, 300]  # Sample data

    # Create a Plotly line chart
    fig = go.Figure(data=go.Scatter(x=years, y=user_counts, mode='lines+markers'))

    # Customize the chart layout
    fig.update_layout(title='User Growth Over Years',
                      xaxis_title='Year',
                      yaxis_title='Number of Users')

    # Convert the Plotly figure to JSON
    graph_data = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return JsonResponse({'graph_data': graph_data})





from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import CustomUser

@api_view(['POST'])
# @permission_classes([AllowAny])
def reset_password(request):
    username = request.data.get('username')
    email = request.data.get('email')
    new_password = request.data.get('new_password')

    try:
        user = CustomUser.objects.get(username=username, email=email)
        
        # Update the user's password
        user.password = make_password(new_password)
        user.save()

        # Send email notification about the password change
        subject = 'Your Password Has Been Changed'
        message = f'Hello {user.username},\n\nYour password has been successfully changed.\n\nIf you did not request this change, please contact support immediately.'
        from_email = 'Policy-Link-Rwanda'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

        return Response({'message': 'Password changed successfully. Please check your email for confirmation.'}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'error': 'Invalid username or email.'}, status=status.HTTP_400_BAD_REQUEST)
