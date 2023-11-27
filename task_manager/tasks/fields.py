from django import forms


class DescriptionField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = forms.Textarea(attrs={
            "class": "form-control", "rows": 10, "cols": 40
            }
        )


class FullNameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()


class NameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name
