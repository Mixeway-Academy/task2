def hidePersonalData(personal_data):
    for char in personal_data:
        personal_data=personal_data.replace(char,"*")
    return personal_data