import hashlib
import base64

def generate_code(serial_number: str) -> str:
    """
    Generates a unique code based on the device's serial number.
    Uses hashing and base64 encoding for a consistent code.
    """
    # Hash the serial number to get a fixed-length code
    hashed_serial = hashlib.sha256(serial_number.encode()).digest()
    # Encode in base64 for a shorter, more readable code
    code = base64.urlsafe_b64encode(hashed_serial).decode('utf-8')[:10]  # Truncate to 10 characters if needed
    return code

def is_password_valid(serial_number: str, password: str) -> bool:
    """
    Checks if the password is compatible with the serial number by decoding.
    The password is valid if it matches the generated code from the serial number.
    """
    expected_code = generate_code(serial_number)
    return password == expected_code




from plyer import uniqueid

def get_device_serial_A():
    return uniqueid.id  # Returns a unique device ID on Android

import platform

print(generate_code(get_device_serial_A()))
