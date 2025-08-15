
#!/usr/bin/env python3
import secrets
import string

def generate_secret_key(length=50):
    characters = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(characters) for _ in range(length))

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("Generated SECRET_KEY:")
    print(secret_key)
    print("\nReplace 'your-secret-key-here-change-this-to-something-secure' in your .env file with the above key")
