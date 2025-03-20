from django import forms

from marketplace.models import Picture


class PicturetFilter(forms.Form):

    class FilterProductForm(forms.Form):
        search = forms.CharField(required=False, label="Поиск", widget=forms.TextInput(attrs={"placeholder": "Введите название"}))
        min_price = forms.DecimalField(required=False, label="Мин. цена")
        max_price = forms.DecimalField(required=False, label="Макс. цена")
        category = forms.ModelChoiceField(queryset=Picture.objects.values_list('category', flat=True).distinct(), required=False, label="Категория")