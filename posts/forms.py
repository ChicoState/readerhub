from django import forms
from posts.models import Post

class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': '10', 'cols': '80'}))

    class Meta():
        model = Post
        fields = [ 'title', 'content', 'created_on', 'last_modified' ]