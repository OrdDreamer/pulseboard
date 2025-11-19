from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import (
    password_validators_help_text_html
)
from django.utils.safestring import mark_safe

User = get_user_model()


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "position",
            "email",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rules = password_validators_help_text_html()
        self.fields["password1"].help_text = mark_safe(
            f'<div class="password-rules">{rules}</div>'
        )
        self.fields["first_name"].widget.attrs.update({"autofocus": True})
        self.fields["username"].widget.attrs.pop("autofocus", None)
