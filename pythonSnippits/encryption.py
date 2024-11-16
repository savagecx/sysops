from cryptography.fernet import Fernet


def encrypt_credentials(key_file_path: str) -> tuple[str, str]:
    """Interactive prompt to encrypt credentials

    Parameters
    ----------
    key_file_path: str
        The path to the key file

    Returns
    -------
    tuple
        A two string tuple containing:
            [0] sec_username: str
                The encrypted username
            [1] sec_password: str
                The encrypted password
    """

    # Create encryption key
    with open(key_file_path, "wb") as key_file:
        key_file.write(Fernet.generate_key())

    # Reopen key as read-only
    with open(key_file_path, "rb") as key_file:
        fernet = Fernet(key_file.read())

    username = input("Username: ")
    password = input("Password: ")

    # Encrypting keys
    sec_username = fernet.encrypt(username.encode()).decode()
    sec_password = fernet.encrypt(password.encode()).decode()

    return sec_username, sec_password


def decrypt_credentials(
    key_file_path: str, sec_username: bytes, sec_password: bytes
) -> tuple[str, str]:
    """Decrypts the credentials stored in the configuration file

    Parameters
    ----------
    key_file_path: str
        The path to the key file
    sec_username: bytes
        The encrypted username
    sec_password: bytes
        The encrypted password

    Returns
    -------
    tuple
        A two string tuple containing:
            [0] Username
            [1] Password
    """

    with open(key_file_path, "rb") as key_file:
        fernet = Fernet(key_file.read())
        username = fernet.decrypt(sec_username).decode()
        password = fernet.decrypt(sec_password).decode()

    return username, password
