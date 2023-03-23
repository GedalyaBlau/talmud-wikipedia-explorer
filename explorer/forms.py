from django import forms

class CommentForm(forms.Form):
    comment_text = forms.CharField(widget=forms.Textarea, label='Comment')


class TextSearchForm(forms.Form):
    talmudic_text_ref = forms.CharField(required=False, label="Talmudic Text Reference")
    wikipedia_article_title = forms.CharField(required=False, label="Wikipedia Article Title")
