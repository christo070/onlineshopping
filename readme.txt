ONLINE SHOPPING SYSTEM

*****************************************************************************************************************************************************
TO BE INSTALLED

1. install python 3
2. it is recommended to setup a virtual environment 
3. pip install django
4. pip install pillow
5. pip install razorpay

*****************************************************************************************************************************************************

STEPS TO EXECUTE

1. In case the zip file has issues, you can clone the project from https://github.com/AkhilMReji/onlineshopping.git
2. change the present working directory to /onlineshopping/
3. python manage.py runserver
4. go to http://127.0.0.1:8000/ or http://localhost:8000/

*****************************************************************************************************************************************************

The credentials of razorpay that we used are from private account of Aditya Wath and hence we have removed the RAZORPAY_API_KEY and the RAZORPAY_API_SECRET from OnlineBazaar/settings.py
Kindly create a new razorpay account(where all the payments of the user will be collected) and generate and use your personal RAZORPAY_API_KEY and RAZORPAY_API_SECRET to see the payment functionality.