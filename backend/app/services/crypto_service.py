import hashlib
import json
import base64
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from backend.app.config import settings

KEY_FILE_PATH = Path(settings.KEY_PATH)

def get_or_create_ed25519_keypair():
    """
    Retrieves or generates a persistent Ed25519 keypair.
    Never exposes the private key to client code.
    """
    KEY_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # If private key hex provided in environment
    if settings.ED25519_PRIVATE_KEY_HEX:
        try:
            priv_bytes = bytes.fromhex(settings.ED25519_PRIVATE_KEY_HEX)
            private_key = ed25519.Ed25519PrivateKey.from_private_bytes(priv_bytes)
            return private_key, private_key.public_key()
        except Exception:
            pass

    # Read from file if exists
    if KEY_FILE_PATH.exists():
        try:
            pem_data = KEY_FILE_PATH.read_bytes()
            private_key = serialization.load_pem_private_key(pem_data, password=None)
            return private_key, private_key.public_key()
        except Exception:
            pass

    # Otherwise generate and persist
    private_key = ed25519.Ed25519PrivateKey.generate()
    pem_data = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    KEY_FILE_PATH.write_bytes(pem_data)
    return private_key, private_key.public_key()


def canonicalize_content(text: str) -> str:
    """
    Canonicalizes content by normalizing line endings and trailing whitespace
    while strictly preserving word and character integrity.
    """
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").split("\n")]
    return "\n".join(lines).strip()


def compute_sha256(text: str) -> str:
    """
    Calculates the hex-encoded SHA-256 hash of canonicalized content.
    """
    canonical = canonicalize_content(text)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def sign_approval_payload(
    submission_id: str,
    version_number: int,
    raw_content: str,
    reviewer_name: str,
    approved_at_iso: str
) -> dict:
    """
    Signs an approval manifest using the server-side Ed25519 private key.
    Returns:
    - canonical_content
    - content_sha256
    - signature_b64
    - public_key_b64
    - payload_dict
    """
    canonical = canonicalize_content(raw_content)
    content_hash = compute_sha256(canonical)

    manifest = {
        "submission_id": submission_id,
        "version_number": version_number,
        "content_sha256": content_hash,
        "reviewer_name": reviewer_name,
        "approved_at": approved_at_iso,
        "issuer": "Inkloom Sentinel — NexaPay Security Authority"
    }

    manifest_bytes = json.dumps(manifest, sort_keys=True).encode("utf-8")
    
    private_key, public_key = get_or_create_ed25519_keypair()
    signature = private_key.sign(manifest_bytes)

    pub_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

    return {
        "canonical_content": canonical,
        "content_sha256": content_hash,
        "signature_b64": base64.b64encode(signature).decode("utf-8"),
        "public_key_b64": base64.b64encode(pub_bytes).decode("utf-8"),
        "manifest": manifest
    }


def verify_approval_signature(
    submission_id: str,
    version_number: int,
    raw_content: str,
    reviewer_name: str,
    approved_at_iso: str,
    signature_b64: str,
    public_key_b64: str
) -> dict:
    """
    Verifies that the content matches the exact SHA-256 hash and that the
    Ed25519 signature is authentic and unaltered.
    """
    canonical = canonicalize_content(raw_content)
    current_hash = compute_sha256(canonical)

    manifest = {
        "submission_id": submission_id,
        "version_number": version_number,
        "content_sha256": current_hash,
        "reviewer_name": reviewer_name,
        "approved_at": approved_at_iso,
        "issuer": "Inkloom Sentinel — NexaPay Security Authority"
    }
    manifest_bytes = json.dumps(manifest, sort_keys=True).encode("utf-8")

    try:
        pub_bytes = base64.b64decode(public_key_b64)
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(pub_bytes)
        sig_bytes = base64.b64decode(signature_b64)

        public_key.verify(sig_bytes, manifest_bytes)
        return {
            "is_valid": True,
            "hash_matches": True,
            "signature_valid": True,
            "current_hash": current_hash,
            "reason": "Cryptographic signature and SHA-256 content hash verified successfully."
        }
    except Exception as e:
        return {
            "is_valid": False,
            "hash_matches": False,
            "signature_valid": False,
            "current_hash": current_hash,
            "reason": f"Cryptographic verification failed: {str(e)}. Content has been altered or signature is invalid."
        }
