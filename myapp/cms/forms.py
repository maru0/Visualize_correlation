from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import forms as auth_forms
# ユーザ作成フォームを継承
from .models import Alldata, Category, Deviation
import pdb


class SignUpForm(UserCreationForm):
    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)


class MessageForm(forms.Form):
    message = forms.CharField(
        label='メッセージ',
        max_length=255,
        required=True,
        widget=forms.TextInput()
    )


class LoginForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label

# ここをカテゴリ情報毎にcheckボックスにする(データベースから引っこ抜く)


class UserForm(forms.Form):
    categories = []
    cate_devi = Alldata.objects.values('cate_id_id', 'static_id_id').distinct()
    for query in cate_devi:
        category_name = Category.objects.get(id=query['cate_id_id'])
        element_name = Deviation.objects.get(id=query['static_id_id'])
        cate_element = str(element_name) + "(" + str(category_name) + ")"
        # pdb.set_trace()
        categories.append((cate_element, cate_element))
    # 同じ名前をタプルでもつ(この値がファイル名)
    ans = forms.MultipleChoiceField(
        label='Category一覧',
        required=True,
        disabled=False,
        initial=['1'],
        choices=categories,
        widget=forms.CheckboxSelectMultiple(attrs={
            'id': 'ans', 'class': 'form-check-input'}))


class CategoryForm(forms.Form):
    name = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple())
