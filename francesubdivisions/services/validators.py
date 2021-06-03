from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from stdnum.exceptions import InvalidChecksum, InvalidFormat, InvalidLength
from stdnum.fr import siren

# Validators
validate_insee_commune = RegexValidator(r"^\d[0-9AB][0-9P]\d\d$")


def validate_siren(value):
    try:
        siren.validate(value)
    except (InvalidChecksum, InvalidFormat, InvalidLength):
        raise ValidationError(
            _("%(value)s is not an valid siren id"),
            params={"value": value},
        )
