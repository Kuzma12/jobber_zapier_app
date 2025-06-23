def validate_and_correct(entry):
    required_fields = ["id", "first_name", "last_name"]
    for field in required_fields:
        if not entry.get(field):
            return False, None, f"Missing required field: {field}"

    entry["first_name"] = entry["first_name"].strip().title()
    entry["last_name"] = entry["last_name"].strip().title()
    return True, entry, None
