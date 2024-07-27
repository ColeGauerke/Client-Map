def get_address_from_company_name(company_name):
    geolocator = Nominatim(user_agent="address_validator")
    try:
        location = geolocator.geocode(company_name)
        if location:
            return f"{location.address}"
        else:
            return None
    except GeocoderTimedOut:
        return None