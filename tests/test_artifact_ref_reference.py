import hashlib

from world_third_reference.artifact_ref import ArtifactRef, verify_artifact_ref


def _ref(path: str, sha256: str = "0" * 64, byte_length: int = 1) -> ArtifactRef:
    return ArtifactRef(relative_path=path, sha256=sha256, byte_length=byte_length)


def test_local_artifact_ref_verifies(tmp_path):
    target = tmp_path / "artifact.json"
    data = b'{"synthetic":true}\n'
    target.write_bytes(data)
    result = verify_artifact_ref(
        ArtifactRef("artifact.json", hashlib.sha256(data).hexdigest(), len(data)),
        local_root=tmp_path,
    )
    assert (result.state, result.reason) == ("VERIFIED_REF", "OK")


def test_parent_escape_is_rejected(tmp_path):
    assert verify_artifact_ref(_ref("../secret.txt"), local_root=tmp_path).reason == "UNSAFE_PATH"


def test_absolute_posix_path_is_rejected(tmp_path):
    assert verify_artifact_ref(_ref("/tmp/secret.txt"), local_root=tmp_path).reason == "UNSAFE_PATH"


def test_windows_drive_path_is_rejected(tmp_path):
    assert verify_artifact_ref(_ref("C:/secret.txt"), local_root=tmp_path).reason == "UNSAFE_PATH"


def test_backslash_path_is_rejected(tmp_path):
    assert verify_artifact_ref(_ref(r"folder\secret.txt"), local_root=tmp_path).reason == "UNSAFE_PATH"


def test_invalid_sha_is_rejected(tmp_path):
    result = verify_artifact_ref(ArtifactRef("artifact.bin", "xyz", 1), local_root=tmp_path)
    assert (result.state, result.reason) == ("NOT_VERIFIABLE", "INVALID_REFERENCE")


def test_negative_byte_length_is_rejected(tmp_path):
    result = verify_artifact_ref(_ref("artifact.bin", byte_length=-1), local_root=tmp_path)
    assert (result.state, result.reason) == ("NOT_VERIFIABLE", "INVALID_REFERENCE")


def test_missing_file_is_not_verifiable(tmp_path):
    result = verify_artifact_ref(_ref("missing.bin"), local_root=tmp_path)
    assert (result.state, result.reason) == ("NOT_VERIFIABLE", "FILE_NOT_FOUND")


def test_byte_length_mismatch_is_tampered(tmp_path):
    data = b"demo"
    (tmp_path / "artifact.bin").write_bytes(data)
    ref = ArtifactRef("artifact.bin", hashlib.sha256(data).hexdigest(), len(data) + 1)
    result = verify_artifact_ref(ref, local_root=tmp_path)
    assert (result.state, result.reason) == ("TAMPERED_REF", "BYTE_LENGTH_MISMATCH")


def test_hash_mismatch_is_tampered(tmp_path):
    data = b"demo"
    (tmp_path / "artifact.bin").write_bytes(data)
    result = verify_artifact_ref(_ref("artifact.bin", byte_length=len(data)), local_root=tmp_path)
    assert (result.state, result.reason) == ("TAMPERED_REF", "HASH_MISMATCH")
