from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UsernameField
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, City, Area


GENDER_LIST = (
        ('', '----Select Gender----'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others')
    )


def getCities():
    cities = City.objects.all()
    return cities


class AddUserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter valid Email Address'}), error_messages={'required': 'Email is Required'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': "password", 'placeholder': 'Enter password'}), error_messages={'required': 'Password cannot be blank'})
    phone = forms.CharField(error_messages={'required': 'Phone number cannot be blank'}, widget=forms.TextInput({'placeholder':  'Phone Number'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter Address'}), min_length=15)
    first_name = forms.CharField(error_messages={'required': 'First Name cannot be left blank'}, widget=forms.TextInput(attrs={'placeholder': 'Enter First Name'}),required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name'}),required=False)
    gender = forms.ChoiceField(choices=GENDER_LIST, widget=forms.Select(attrs={'placeholder': 'Gender'}), initial='')
    city = forms.ModelChoiceField(getCities(), widget=forms.Select(attrs={'id': "city"}), initial='')
    is_student = forms.BooleanField(widget=forms.CheckboxInput(attrs={'placeholder': 'Student'}), label="Student", initial=True, required=False)
    is_pgVendor = forms.BooleanField(widget=forms.CheckboxInput(attrs={'placeholder': 'PG Vendor'}), label="PG Vendor", required=False)
    is_foodVendor = forms.BooleanField(widget=forms.CheckboxInput(attrs={'placeholder': 'Food Vendor'}), label="Food Vendor", required=False)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.object.filter(email=email).exists():
            raise forms.ValidationError('Email Already in Use !!')
        
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            try:
                validate_password(password)
            except forms.ValidationError as error:
                self.add_error("password", "Invalid Password")
            return password
        else:
            raise forms.ValidationError("Enter password")
        
    def save(self):
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        password = self.cleaned_data.get('password')
        gender = self.cleaned_data.get('gender')
        address = self.cleaned_data.get('address')
        phone = self.cleaned_data.get('phone')
        is_student = self.cleaned_data.get('is_student')
        is_pgVendor = self.cleaned_data.get('is_pgVendor')
        is_foodVendor = self.cleaned_data.get('is_foodVendor')
        area_id = self.cleaned_data.get('area_id')
        return User.object.create_user(first_name, last_name, email, password, gender, address, phone, is_pgVendor,is_foodVendor, is_student, area_id)
        
    class Meta:
        model = User
        exclude = ('last_login', 'is_superuser', 'groups', 'user_permissions', 'email_verified_at', 'is_active', 'is_staff', 'avatar', 'date_joined')

    field_order = ['email', 'password', 'first_name', 'last_name', 'address', 'phone', 'gender', 'city', 'area_id' ,'is_student', 'is_pgVendor', 'is_foodVendor']


class CustomUserCreationForm(UserCreationForm):
    # """A form for creating new users. Includes all the required
    # fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    # email = forms.EmailField(widget=forms.EmailInput)
    
    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')
    
        # Check to see if any users already exist with this email as a username.
        try:
            match = User.object.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email
    
        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')
    
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    #

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'address', 'is_active')
        # field_classes = {'username': UsernameField}
    #
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('../password/')
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')
    
        # Check to see if any users already exist with this email as a username.
        try:
            match = User.object.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email
    
        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        # user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
