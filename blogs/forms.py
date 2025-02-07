from django import forms
from .models import Topic, Post, Comments

class CreatePost(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic'].empty_label = 'Select topic'
        
    class Meta:
        model = Post
        fields = ['topic','title','description']
        widgets = {
            'topic':forms.Select(attrs={
                'class':'form-select'
            }),
            'title':forms.TextInput(attrs={
                'class':'form-control',
            }),
            'description':forms.Textarea(attrs={
                'class':'form-control',
                'rows':'7'
            })
        }   
    
class SharePost(forms.Form):
    to = forms.EmailField(required=False, label='Email')
    message = forms.CharField(max_length=255, required = True, widget = forms.Textarea())
    
    to.widget.attrs.update({"class":'form-control my-3',
                            "id":'share_email',
                            "placeholder":'name@example.com',
                            })
    message.widget.attrs.update({"class":'form-control  my-3',
                                 "placeholder":"Message...",})
    

class CommentPost(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['message']
        widgets = {
            'message':forms.Textarea(attrs={
                'class':'form-control rounded-5 my-3 bg-ligth',
                'rows':'1',
                'placeholder':'Comments....'
            })
            }
        
