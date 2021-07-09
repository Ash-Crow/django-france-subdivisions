from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from stdnum.exceptions import InvalidChecksum, InvalidFormat, InvalidLength
from stdnum.fr import siren


validate_insee_region = RegexValidator(r"^\d\d$")
validate_insee_departement = RegexValidator(
    r"^([0-1]\d|2[AB1-9]|[3-8]\d|9[0-5]|97[12346])$"
)
validate_insee_commune = RegexValidator(r"^\d[0-9AB][0-9P]\d\d$")


def validate_siren(value):
    try:
        siren.validate(value)
    except (InvalidChecksum, InvalidFormat, InvalidLength):
        raise ValidationError(
            _("%(value)s is not a valid siren id"),
            params={"value": value},
        )
