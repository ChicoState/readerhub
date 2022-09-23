from django import forms
from personalization.models import PersonalInfo




class PersonalInfoForm(forms.ModelForm):
	favorite_books = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
	about_user = forms.CharField(widget=forms.Textarea(attrs={'rows': '9' , 'cols': '80'}))

	class Meta():
		model = PersonalInfo
		fields = [ 'favorite_books','about_user', 'personal_image']
