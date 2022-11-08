from django.core.exceptions import ValidationError


def validate_max_flat(current_flat, max_flat):
    if current_flat > max_flat & current_flat < 1:
        raise ValidationError("Вы ввели неверный номер квартиры")
    else:
        return current_flat

