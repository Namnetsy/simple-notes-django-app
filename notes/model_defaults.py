from django.db import models
from django.utils.translation import gettext as _


class Theme(models.TextChoices):
    DEFAULT = "default", _("Default")
    LUX = "lux", _("Lux")
    PULSE = "pulse", _("Pulse")
    SANDSTONE = "sandstone", _("Sandstone")


class Language(models.TextChoices):
    UK = "uk", _("Українська")
    EN = "en", _("English")
