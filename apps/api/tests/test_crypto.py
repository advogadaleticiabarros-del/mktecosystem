from app.core.crypto import decrypt_token, encrypt_token


def test_encrypt_decrypt_roundtrip():
    original = "EAAG_token_de_exemplo_super_secreto"
    ciphertext = encrypt_token(original)
    assert ciphertext != original
    assert decrypt_token(ciphertext) == original
