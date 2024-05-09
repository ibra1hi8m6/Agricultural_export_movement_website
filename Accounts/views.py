from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User,Group,Permission
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from django.utils.timezone import datetime, timedelta
from http.cookies import SimpleCookie
from Accounts.models import CustomUser 
from Products.models import *
# Create your views here.
def AboutPage(request):
    
    return render(request, 'Account_html/about.html')
def ContactUsPage(request):
    
    return render(request, 'Account_html/contact-us.html')
def exporterprofile(request  ,user_id ):
        Exporter = get_object_or_404(CustomUser, id=user_id) 
        products = Product.objects.filter(user_id=user_id)
        return render(request, 'Account_html/exporterprofile.html', {'products': products,'Exporter': Exporter})
    





def importerprofile(request, user_id):
    Importer = get_object_or_404(CustomUser, id=user_id)  # Use CustomUser instead of User
    return render(request, 'Account_html/importerprofile.html', {'Importer': Importer})




def SignUpPage(request):

    
    if request.method == "POST":
        # username = request. POST get('username' )
        username = request. POST['username' ]
        fname = request. POST['fname' ]
        Iname = request. POST['lname']
        email = request.POST['email']
        user_type = request.POST['Types']
        phone = request.POST['phone']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        address=request.POST['address'] 
        TaxCard=request.POST['Tax card'] 
        CommercialRegister=request.POST['comm'] 


# Check if username or email already exist
        if get_user_model().objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'registration/SignUp.html')
        if get_user_model().objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, 'registration/SignUp.html')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            
        else :
            User = get_user_model()
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser. last_name = Iname
            myuser.address = address
            myuser.CommercialRegister=CommercialRegister
            myuser.TaxCard=TaxCard
            myuser.phone = phone
            
            # Assign user to a group and grant permission based on user type
            # Assign user to a group based on user type
            if user_type == 'Exporter':
                exporter_group, created = Group.objects.get_or_create(name='Exporter')
                myuser.groups.add(exporter_group)

                # Grant permission for the "add_product" view
                permission = Permission.objects.filter(codename='add_product')[0]  # Replace with actual permission codename
                myuser.user_permissions.add(permission)

            myuser. save()
            login (request, myuser)
            return redirect( '/' )

    return render(request, 'registration/SignUp.html')



# def loginPage(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('pass1')
#         user = authenticate(username=username, password=password)

#         if user is not None:
#             login(request, user)
#             if user.groups.filter(name='Exporter').exists():
#                 return redirect('exporterprofile', user.id) 
#             # Generate or get the token for the user
#             token, created = Token.objects.get_or_create(user=user)
#             # Print or log the token
#             print(f"User Token: {token.key}")
            
#             # Set the token as an HTTP-only cookie
            
#         else:
#             login(request, user)
#             return redirect('/')

#     return render(request, 'registration/login.html')

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass1')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if user.groups.filter(name='Exporter').exists():
                return redirect('exporterprofile', user.id) 
            elif user.is_superuser:
                return redirect('add_category')  # Assuming 'add_category' is the URL name for the add category page
            else:
                return redirect('/')
        else:
            return redirect('/')  # Redirect if authentication fails

    return render(request, 'registration/login.html')



def logoutPage(request):
    # Delete the user's token when logging out
    if request.user.is_authenticated:
        from rest_framework.authtoken.models import Token
        Token.objects.filter(user=request.user).delete()

        # Delete the token cookie on the client side
        response = HttpResponse()

        # Create a SimpleCookie and set an expired cookie with the same name
        cookie = SimpleCookie()
        cookie['token'] = ''
        cookie['token']['expires'] = datetime.utcnow() - timedelta(days=1)
        response.headers['Set-Cookie'] = str(cookie)

        logout(request)
        return redirect('/')  # Redirect to the home page

    return redirect('/')