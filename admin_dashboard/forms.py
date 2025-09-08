from django import forms
from core.models import AllowedUser

class AllowedUserForm(forms.ModelForm):
    class Meta:
        model = AllowedUser
        fields = ['email', 'role', 'is_active']
        widgets = {
            'role': forms.Select(choices=AllowedUser.ROLE_CHOICES),
        }

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        qs = AllowedUser.objects.filter(email__iexact=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This email is already in the allowed list.")
        return email