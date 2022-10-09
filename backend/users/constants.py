from django.utils.translation import gettext_lazy as _


class Messages(object):
    INVALID_CREDENTIALS_ERROR = _(
        "Невозможно войти с предоставленными учетными данными."
    )
    INACTIVE_ACCOUNT_ERROR = _("Учетная запись пользователя отключена.")
    INVALID_TOKEN_ERROR = _("Недопустимый токен для данного пользователя.")
    INVALID_UID_ERROR = _(
        "Недопустимый ID пользователя или пользователь не существует."
    )
    STALE_TOKEN_ERROR = _("Устаревший токен для данного пользователя».")
    PASSWORD_MISMATCH_ERROR = _("Два поля пароля не совпадают.")
    USERNAME_MISMATCH_ERROR = _("Два {0} поля не совпадают.")
    INVALID_PASSWORD_ERROR = _("Неверный пароль")
    EMAIL_NOT_FOUND = _(
        "Пользователь с указанным адресом электронной почты не существует."
    )
    CANNOT_CREATE_USER_ERROR = _("Не удалось создать учетную запись.")