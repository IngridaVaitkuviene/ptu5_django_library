from django import forms
from . models import BookReview
from django.utils.timezone import datetime, timedelta


class BookReviewForm(forms.ModelForm):
    def is_valid(self):
        valid = super().is_valid()
        if valid:
            reader = self.cleaned_data.get("reader")
            recent_posts = BookReview.objects.filter(reader=reader, created_at__gte=(datetime.now() - timedelta(days=1)))
            print(recent_posts)
            if recent_posts:
                return False
        return valid

    class Meta:
        model = BookReview
        fields = ('content', 'book', 'reader')
        widgets = {
            'book': forms.HiddenInput(),
            'reader': forms.HiddenInput(),
        }