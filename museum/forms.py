from django import forms
from .models import VisitorComment, Highlight

class VisitorCommentForm(forms.ModelForm):
    class Meta:
        model = VisitorComment
        fields = ['comment', 'rating']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share your thoughts about the museum...',
                'rows': 4
            }),
            'rating': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'comment': 'Your Comment',
            'rating': 'Rating (1-5 stars)'
        }

class HighlightForm(forms.ModelForm):
    class Meta:
        model = Highlight
        fields = [
            'title', 'description', 'video_url', 'video_file', 'thumbnail',
            'tournament', 'player', 'moment_type', 'duration', 'is_featured'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название хайлайта'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание момента',
                'rows': 4
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://youtube.com/...'
            }),
            'video_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'video/*'
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'tournament': forms.Select(attrs={'class': 'form-control'}),
            'player': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Игрок или команда'
            }),
            'moment_type': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0:15'
            }),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'video_url': 'YouTube/Vimeo ссылка',
            'video_file': 'Или загрузите видео файл',
            'thumbnail': 'Превью (опционально)'
        }
    
    def clean(self):
        cleaned_data = super().clean()
        video_url = cleaned_data.get('video_url')
        video_file = cleaned_data.get('video_file')
        
        if not video_url and not video_file:
            raise forms.ValidationError("Укажите ссылку на видео или загрузите видео файл")
        
        return cleaned_data