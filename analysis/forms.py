from django import forms

class MonthlyAnalysisForm(forms.Form):
    keyword = forms.TextInput()