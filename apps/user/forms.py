from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext as _

from .models import Usuario


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Senha'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Confirmação de senha'), widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('email', 'name',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("As senhas informadas não são iguais."))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label= ("Senha"),
        help_text= ("Esta é a senha criptografada do usuário, mas você pode alterar "
                    "acessando <a href=\"../password/\">este formulário</a>."))

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)

        self.fields['groups'].required = True

    class Meta:
        model = Usuario
        fields = '__all__'

    def clean_password(self):
        return self.initial["password"]
