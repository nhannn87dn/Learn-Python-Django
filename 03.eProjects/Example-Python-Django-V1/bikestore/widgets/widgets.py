from django import forms

class CustomTextInput(forms.TextInput):
    def __init__(self, attrs=None):
        default_attrs = {'class': 'form-control', 'placeholder': 'Enter text here'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

    def render(self, name, value, attrs=None, renderer=None):
        # Custom rendering logic if needed
        return super().render(name, value, attrs, renderer)

class CustomEmailInput(forms.EmailInput):
    def __init__(self, attrs=None):
        default_attrs = {'class': 'form-control', 'placeholder': 'Enter your email'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

    def render(self, name, value, attrs=None, renderer=None):
        # Custom rendering logic if needed
        return super().render(name, value, attrs, renderer)

class CustomRadioSelect(forms.RadioSelect):
    def __init__(self, attrs=None):
        default_attrs = {'class': 'custom-radio-select'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

    def render(self, name, value, attrs=None, renderer=None):
        # Custom rendering logic if needed
        return super().render(name, value, attrs, renderer)