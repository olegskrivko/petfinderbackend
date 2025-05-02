# # from py_vapid import Vapid01
# # import base64
# # from cryptography.hazmat.primitives import serialization

# # # Create VAPID instance
# # vapid = Vapid01()

# # # Generate key pair
# # vapid.generate_keys()

# # # Serialize private and public keys to bytes
# # private_key_bytes = vapid._private_key.private_bytes(
# #     encoding=serialization.Encoding.PEM,
# #     format=serialization.PrivateFormat.PKCS8,
# #     encryption_algorithm=serialization.NoEncryption()
# # )

# # public_key_bytes = vapid._public_key.public_bytes(
# #     encoding=serialization.Encoding.PEM,
# #     format=serialization.PublicFormat.SubjectPublicKeyInfo
# # )

# # # Base64 encode the keys (URL-safe encoding)
# # private_key_b64 = base64.urlsafe_b64encode(private_key_bytes).decode('utf-8')
# # public_key_b64 = base64.urlsafe_b64encode(public_key_bytes).decode('utf-8')

# # # Print the keys
# # print("✅ Public VAPID Key (for React):")
# # print(public_key_b64)
# # print("\n🔐 Private VAPID Key (for Django backend):")
# # print(private_key_b64)
# # from py_vapid import Vapid01
# # import base64
# # from cryptography.hazmat.primitives import serialization

# # # Create VAPID instance
# # vapid = Vapid01()

# # # Generate key pair
# # vapid.generate_keys()

# # # Serialize private and public keys to bytes
# # private_key_bytes = vapid._private_key.private_bytes(
# #     encoding=serialization.Encoding.PEM,
# #     format=serialization.PrivateFormat.PKCS8,
# #     encryption_algorithm=serialization.NoEncryption()
# # )

# # public_key_bytes = vapid._public_key.public_bytes(
# #     encoding=serialization.Encoding.PEM,
# #     format=serialization.PublicFormat.SubjectPublicKeyInfo
# # )

# # # Base64 encode the keys (URL-safe encoding)
# # private_key_b64 = base64.urlsafe_b64encode(private_key_bytes).decode('utf-8')
# # public_key_b64 = base64.urlsafe_b64encode(public_key_bytes).decode('utf-8')

# # # Write the keys to a .txt file with UTF-8 encoding
# # file_path = 'vapid_keys.txt'

# # with open(file_path, 'w', encoding='utf-8') as f:
# #     f.write("✅ Public VAPID Key (for React):\n")
# #     f.write(public_key_b64 + "\n\n")
# #     f.write("🔐 Private VAPID Key (for Django backend):\n")
# #     f.write(private_key_b64 + "\n")

# # print(f"Keys have been successfully written to {file_path}")
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

# # Get the raw public key bytes from the public key object
# public_key_bytes = vapid._public_key.public_bytes(
#     encoding=serialization.Encoding.DER,
#     format=serialization.PublicFormat.SubjectPublicKeyInfo
# )

# # Base64 URL-safe encode the raw public key bytes (NOT the PEM formatted key)
# public_key_b64 = base64.urlsafe_b64encode(public_key_bytes).decode('utf-8')

# # Base64 URL-safe encode the private key (for Django backend, keeping PEM format)
# private_key_b64 = base64.urlsafe_b64encode(private_key_bytes).decode('utf-8')

# # Write the keys to a .txt file with UTF-8 encoding
# file_path = 'vapid_keys.txt'

# with open(file_path, 'w', encoding='utf-8') as f:
#     f.write("✅ Public VAPID Key (for React):\n")
#     f.write(public_key_b64 + "\n\n")
#     f.write("🔐 Private VAPID Key (for Django backend):\n")
#     f.write(private_key_b64 + "\n")

# print(f"Keys have been successfully written to {file_path}")
import base64
import ecdsa

def generate_vapid_keypair():
  """
  Generate a new set of encoded key-pair for VAPID
  """
  pk = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
  vk = pk.get_verifying_key()

  return {
    'private_key': base64.urlsafe_b64encode(pk.to_string()).strip(b"="),
    'public_key': base64.urlsafe_b64encode(b"\x04" + vk.to_string()).strip(b"=")
  }

keypair = generate_vapid_keypair()

print(f"Private:\n\n{keypair['private_key'].decode('utf-8')}\n")
print(f"Public:\n\n{keypair['public_key'].decode('utf-8')}\n")

# Private:

# 6A4B3w6RGZjFS1iZA43a7LNknA-dhZau1CitGIW33GM

# Public:

# BOZTcqsdJXUbELTV3ax5lK3X3Wh4S33MuJAZ75MVWCxjtrcn7nVr2Xp-JPiPlVJCE9gqmLv23_PR_f-7uKgU8iU