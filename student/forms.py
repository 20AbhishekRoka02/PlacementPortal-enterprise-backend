from django import forms
from .models import Resume
import json


class ResumeForm(forms.ModelForm):

    JSON_FIELDS = ["social_media", "education", "experience", "projects"]

    class Meta:
        model = Resume
        fields = [
            "name",
            "email",
            "phone",
            "social_media",
            "education",
            "experience",
            "projects",
            "misc_title",
            "misc_description",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Full Name"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email"
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Phone Number"
            }),

            "social_media": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": '[{"type": "linkedin", "url": "..."}]',
                "rows": 3
            }),
            "education": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": '[{"degree": "B.Tech", "college": "...", "year": "..."}]',
                "rows": 4
            }),
            "experience": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": '[{"company": "...", "role": "...", "duration": "..."}]',
                "rows": 4
            }),
            "projects": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": '[{"title": "...", "description": "..."}]',
                "rows": 4
            }),

            "misc_title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Extra Section Title"
            }),
            "misc_description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Extra Details",
                "rows": 3
            }),
        }

    # -------------------------------
    # CLEAN ALL JSON FIELDS TOGETHER
    # -------------------------------
    def clean(self):
        cleaned_data = super().clean()

        for field in self.JSON_FIELDS:
            value = cleaned_data.get(field)

            if not value:
                cleaned_data[field] = []
                continue

            if isinstance(value, str):
                try:
                    cleaned_data[field] = json.loads(value)
                except json.JSONDecodeError:
                    self.add_error(field, "Must be valid JSON format (list or object)")
                    cleaned_data[field] = []

            elif not isinstance(value, (list, dict)):
                self.add_error(field, "Must be JSON list or object")
                cleaned_data[field] = []

        return cleaned_data

    # -------------------------------
    # SAFE SAVE METHOD
    # -------------------------------
    def save(self, commit=True, student=None):
        instance = super().save(commit=False)

        if student:
            instance.student = student

        if instance.student is None:
            raise ValueError("Student is required to create a Resume")

        if commit:
            instance.save()

        return instance