from django import forms


def validate_not_empty(value):
    if value == '':
        raise forms.ValidationError(
            'Молчание – золото, но не в этом случае!',
            params={'value': value})
