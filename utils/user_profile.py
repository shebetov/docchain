

def get_profile_type(user):
    if getattr(user, 'patient_profile', None) is not None:
        return 'patient'
    elif getattr(user, 'doctor_profile', None) is not None:
        return 'doctor'
    return None