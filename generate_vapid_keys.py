# from py_vapid import Vapid01
# import base64
# from cryptography.hazmat.primitives import serialization

# # Create VAPID instance
# vapid = Vapid01()

# # Generate key pair
# vapid.generate_keys()

# # Serialize private and public keys to bytes
# private_key_bytes = vapid._private_key.private_bytes(
#     encoding=serialization.Encoding.PEM,
#     format=serialization.PrivateFormat.PKCS8,
#     encryption_algorithm=serialization.NoEncryption()
# )

# public_key_bytes = vapid._public_key.public_bytes(
#     encoding=serialization.Encoding.PEM,
#     format=serialization.PublicFormat.SubjectPublicKeyInfo
# )

# # Base64 encode the keys (URL-safe encoding)
# private_key_b64 = base64.urlsafe_b64encode(private_key_bytes).decode('utf-8')
# public_key_b64 = base64.urlsafe_b64encode(public_key_bytes).decode('utf-8')

# # Print the keys
# print("✅ Public VAPID Key (for React):")
# print(public_key_b64)
# print("\n🔐 Private VAPID Key (for Django backend):")
# print(private_key_b64)
# from py_vapid import Vapid01
# import base64
# from cryptography.hazmat.primitives import serialization

# # Create VAPID instance
# vapid = Vapid01()

# # Generate key pair
# vapid.generate_keys()

# # Serialize private and public keys to bytes
# private_key_bytes = vapid._private_key.private_bytes(
#     encoding=serialization.Encoding.PEM,
#     format=serialization.PrivateFormat.PKCS8,
#     encryption_algorithm=serialization.NoEncryption()
# )

# public_key_bytes = vapid._public_key.public_bytes(
#     encoding=serialization.Encoding.PEM,
#     format=serialization.PublicFormat.SubjectPublicKeyInfo
# )

# # Base64 encode the keys (URL-safe encoding)
# private_key_b64 = base64.urlsafe_b64encode(private_key_bytes).decode('utf-8')
# public_key_b64 = base64.urlsafe_b64encode(public_key_bytes).decode('utf-8')

# # Write the keys to a .txt file with UTF-8 encoding
# file_path = 'vapid_keys.txt'

# with open(file_path, 'w', encoding='utf-8') as f:
#     f.write("✅ Public VAPID Key (for React):\n")
#     f.write(public_key_b64 + "\n\n")
#     f.write("🔐 Private VAPID Key (for Django backend):\n")
#     f.write(private_key_b64 + "\n")

# print(f"Keys have been successfully written to {file_path}")
from py_vapid import Vapid01
import base64
from cryptography.hazmat.primitives import serialization

# Create VAPID instance
vapid = Vapid01()

# Generate key pair
vapid.generate_keys()

# Serialize private and public keys to bytes
private_key_bytes = vapid._private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Get the raw public key bytes from the public key object
public_key_bytes = vapid._public_key.public_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Base64 URL-safe encode the raw public key bytes (NOT the PEM formatted key)
public_key_b64 = base64.urlsafe_b64encode(public_key_bytes).decode('utf-8')

# Base64 URL-safe encode the private key (for Django backend, keeping PEM format)
private_key_b64 = base64.urlsafe_b64encode(private_key_bytes).decode('utf-8')

# Write the keys to a .txt file with UTF-8 encoding
file_path = 'vapid_keys.txt'

with open(file_path, 'w', encoding='utf-8') as f:
    f.write("✅ Public VAPID Key (for React):\n")
    f.write(public_key_b64 + "\n\n")
    f.write("🔐 Private VAPID Key (for Django backend):\n")
    f.write(private_key_b64 + "\n")

print(f"Keys have been successfully written to {file_path}")
