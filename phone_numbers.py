import phonenumbers


phones = [
    "+55 11 99999-9999",
    "+55 11 2999-9999",
    "5531938959855",
    "553138959855",
    "+55 (31) 93892-9068",
    "+55 (31) 3892-9068",
    "(31) 93892-9068",
    "(31) 3892-9060",
    "35931929626",
    "3531929620"
]

formated_phones = []

def format_phone(phone, country="BR"):
    try:
        parsed_phone = phonenumbers.parse(phone, country)
        if phonenumbers.is_valid_number(parsed_phone):
            return phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.NATIONAL)
        else:
            return phone
    except phonenumbers.NumberParseException:
        return phone
    
for phone in phones:
    formated_phones.append(format_phone(phone))

print(formated_phones)