# services/specialist_service.py
user_is_specialist = None


def set_specialist(value: bool):
    global user_is_specialist
    user_is_specialist = value


def get_specialist():
    return user_is_specialist
