from django import forms
import re
from django.forms import ModelForm
from blog.models import Post
from tinymce.widgets import TinyMCE

class ContactForm(forms.Form):
    countries = [
        ('IN', 'India'),
        ('US', 'United States'),
    ]
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'name-field'}))
    email = forms.EmailField(required=False)
    phone_no = forms.RegexField(regex="^[6-9][0-9]{9}$", required=False)
    message = forms.CharField(max_length=500, widget=forms.Textarea)
    country = forms.ChoiceField(choices = countries)

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data['phone_no']
        email = cleaned_data['email']

        if phone == '' and email == '':
            #raise forms.ValidationError("Email or Phone 1 should be field", code='invalid')
            self.add_error("phone_no", "Email or Phone 1 should be field")

    # def clean_password(self):
    #     password = self.cleaned_data['password']
    #     r = re.search('[A-Z][a-z][0-9]', password)

    #     if not r:
    #         raise forms.ValidationError("1 Upper, 1Lower, 1Special 1Num", code="upper")
    #     else:
    #         return password

class PostForm(ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    author = forms.CharField(disabled=True)

    class Meta:
        model = Post
        fields = ['title', 'content', 'status', 'category', 'image']