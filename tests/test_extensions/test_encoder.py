from hypothesis import given
from hypothesis import strategies as st
from pytest_bdd_report.extensions.encoder import Base64Encoder


@given(st.binary())
def test_encode_decode(image_bytes: bytes) -> None:
    encoded_image = Base64Encoder.encode(image_bytes)

    decoded_image = Base64Encoder.decode(encoded_image)
    assert decoded_image == image_bytes
