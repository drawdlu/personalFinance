# Personal Finance Tracker
#### Video Demo:  https://www.youtube.com/watch?v=iaxffZCyqZI
#### Description:

This is an account tracker that allows users to track their finances every month. 

## I've created 6 models for this project at main/models.py (I'm using the built in User model in Django)
### Accounts
Track all of users bank accounts, e-wallets, source of funds
The balance of each account is also tracked
### Category
Tracks all of the users categories to be used for each transaction made
### Debit
Tracks all of the users debit transaction information
- date
- amount
- description
- account
- category
### Credit
Tracks all of the users credit transaction information
- the same information is saved as *Debit*, the only difference is the amount is a positive decimal while it is negative in *Debit*
### MonthYear
Tracks what month-year the user has transactions on
### UserProfile
Currently only tracks the users preferred currency. I named it *UserProfile* in case I want to track user specific data other than *currency* in the future.


## This part of the app is only accessible to a user who is not logged in
I've implemented this using an *if statement* at specific functions in *register/views.py* which redirects users to the homepage if they are logged in

### Login Page
users can login to an existing account, go to the register page, or click a link to recover a forgotten password
### Registration Page
At the register page users can register with the following fields (which are all required):
- Username
- Email Address
- Password and a password confirmation
After registering a confirmation email will be sent to the user
- only after clicking the confirmation link will the user be able to login
### Password Reset Page
If a user clicks a password reset button they will be given a form to enter their email for password recovery
- once the password recovery email is clicked they will be asked to type a new password twice for confirmation

## This part of the app is only accessible to a user who is logged in
I've implemented this using *Django's* built in *decorator* `@login_required`

### Homepage
On the homepage the data for the current month is displayed, a balance sheet, total amount transacted through each account, list of all transactions, and a form to add a new transaction. 
### History Page
On the history page user can choose a month-year from a dropdown form to display the same thing on the homepage except the ability to add a transaction
- the dropdown will only display month-years where you have had transactions on, even if those transactions no longer exists (if you have deleted them)
### Accounts Page
On the accounts page you can add and edit accounts and categories to track
### Search Bar
At the search bar on the menu you can search the database for transactions based on the keywords you type
- the keyword will be searched on descriptions, categories, and accounts
### Profile Page
On the profile page your email and username will be displayed
- you also have the option here to change your password or change the currency used on your account


## Registration and Email Confirmation
At *register/views.py* 
### Register
The first thing that will be returned when you visit the registration page is a form for registration. If the user has registered successfully given that the username and email address are unique and valid, the details the user has entered will be saved and `is_active` will be set to `False` (this will be returned back to `True` only after the user has confirmed email successfully). The function will then call on *emailActivation* (while passing the needed parameters) for email activation.
- We also create a *UserProfile* at register where the default value of currency is set to a *$* dollar sign
### Email Activation
This function will compose the email subject and message (together with the *token* and *email of user*) and save it to an *email* variable. It will then try to send it to the *email* you provided and display a message of success or failure.
### Activate
Which is handled by this path `"activate/<uidb64>/<token>"` which is triggered when user clicks and activation link. It checks first if the user exists and if the token is valid then it changes `is_active` to `True`

## Password Reset
At *register/views.py* 
### password_reset
This function behaves similar to *emailActivation*, when a form is submitted it composes an email and sends it to the *email* input by the user.
- It also checks if the *email* entered is associated with any user in the database
### passwordResetConfirm
Which is handled by this path `'reset/<uidb64>/<token>'` which is triggered when a user clicks on a password reset link in their email. This function behaves similar to *activate*, when a user clicks on password reset link it checks first if user exists and if the token is valid then renders a password reset form. When a user clicks submit the new password hash is saved to the User model.

## Token
At *register/token.py*
We create a token generator which will be used for *emailActivation* and *password_reset*

## Login 
It is handled by *Django*, we do not use a specific view function to render the form for login. We just need to put the html file at *register/templates/registration* and it will handle the form automatically.

## Homepage
This is where we render the current month's tables for *Balance Sheet*, *Account Summary*, *Transactions*. We also have a single form where the user can add transactions.
### Transaction Form
All fields of the form are required. We use a date widget for entering the date.
We use the same form for *debit* and *credit* transactions and we handle the input based on what button the user has pressed. 
- when a transaction is added we also add that month-year if it does not exist in the users *MonthYear* table
	- the day is always saved to 1 before it is saved because we are only interested in the month and year
### Transactions
The transactions are rendered through two tables, *debit* and *credit*. We use `datetime.now()` to get the date today and filter the users *debit* and *credit* tables based on current month and year. This filtered result is then passed through to the template while adding a *delete* button at the end of every transaction information.
### Balance Sheet and Account Summary
The balance sheet data are taken from the filtered data used in *transactions* which is then passed to the *get_summary* function in *helper.py* which returns 3 things (total per category, overall total, and total per account). The filtered *debit* and *credit* data is passed through this function to get the data for the *balance sheet*.
- *get_summary* looks at each transaction and checks whether the category or account exists in each given dictionary, if it does not exists it adds the category or account and sets the amount to the current transaction, if it does exists it adds the amount to the specific category or account in the given dictionary. While doing so, it adds every transaction to get the total in *debit* or *credit* (depending on which data has been passed)
	- after looking at each transaction it returns the overall transaction total, category total, and account total

## Accounts Page
This is where you can add and edit *accounts* and *categories* 
### Adding Accounts
Each account is unique for each user only, we handle adding an account which already exists through a try in *IntegrityError*. If the account name already exists we tell the user using `messages.info`
- when adding an account we also prompt the user to add an initial balance
- the form we use for this just uses `ModelForm` on the *Accounts* object
### Editing Accounts
There are no required fields on editing accounts form. Users can choose to only edit the name or the balance or both. The only required field is choosing which account they want to edit.
- To generate the form we pass in all of current users accounts to the form to provide data for the dropdown menu
	- if we don't do this the form fill generate a dropdown of all accounts from all users
- When editing and adding accounts we always make sure it is in *upper case*, this is a design choice to handle *unique* *accounts* and *categories* better
### Adding and Editing Categories
Adding and editing categories uses the same logic as adding and editing accounts, the only main difference is that accounts has an extra value which is the *balance*
### Rendering Accounts and Categories in HTML
We don't need to pass through data to render accounts and categories. We can access the users model objects directly through the Django Template syntax
Ex. `user.category.all`, `user.accounts.all`

## History Page
### Date Dropdown Form
We generate the dropdown list based on the users *MonthYear* data which is always updated on the first transaction of the month. 
### Rendering History Based on User Input
When a user chooses a date and clicks on the *display button* the page will generate transactions for that month. We generate this similarly to how we generate the homepage except the date is filtered based on the user input instead of the date today.

## Search
Search is done on all of users transactions (both *debit* and *credit*) *account_name* , *category_name*, *description*.
- We handle search be using `.filter` function 
- We also make sure that we set each search on debit and credit (category or account) to check for *IndexError*, which means the category or account doesn't exist and we need to create the queryset objects and assign none to it. 
	- We do this to prevent an error when we try to combine results of all searches later on.
- Checking the description is the easiest because we don't have to deal with *foreign keys* and just filter for the keyword directly on the object
- We order the results based on the most recent dates
- An *if else* statement is then used to check if any data was found and if not, tell the user that nothing was found

## Delete
We handle transaction deletion by passing the *transaction id* through the url which is then handled by the path `"<int:id>"`
- The first thing we check is if the object exists, in case of errors
- Then we check whether the user is trying to delete a *credit* or a *debit* which we can extract because we used a hidden input to differentiate the one from the other.
- Deleting then is kind of straight forward, we delete the transaction based on the id then we update the balance of the account based on the type of transaction
	- We add the amount back to the account if it was a *debit*
	- We subtract the amount if it was a *credit*

## Profile
The profile handles only 3 things which is displaying user data (email, username), changing password, and changing preferred currency to use.
### Changing password while logged in
When the change password link in the profile page is clicked the user is redirected to a page which prompts for a password, similar to when users try to recover a password through an email except the password is changed immediately when a user inputs a valid password and submits the form.
### Changing Preferred Currency
The form generated contains only one field which allows users to choose from a tuple of currencies hard coded into *main/forms.py*. When a user chooses a currency and clicks submit the *UserProfile* of the logged in user is updated to the currency chosen.

## Extra Installation
### settings.py
``` python
# at installed apps
'crispy_forms',
'crispy_bootstrap5',
'mathfilters',


# for crispy form usage
CRISPY_TEMPLATE_PACK="bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

# login and logout redirect
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login"

# email setup
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_FROM = 'apptestcontrol@gmail.com'
EMAIL_HOST_USER = 'apptestcontrol@gmail.com'
EMAIL_HOST_PASSWORD = 'tefu imzo tgmw lrlt'
EMAIL_PORT = 587

PASSWORD_RESET_TIMEOUT = 14400
```

```
$ pip install django-mathfilters
$ pip install django-crispy-forms
```

## Languages used
- HTML
- CSS
- Python
	- Django 
	- Django Templates
- A bit of JavaScript