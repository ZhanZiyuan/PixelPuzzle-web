#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Encode/decode images using Base64
or shuffle/recover the pixels of images.
"""

import hashlib
import os
import secrets
from base64 import b64decode, b64encode
from pathlib import Path

import numpy as np
from flask import (Flask, Response, make_response, render_template, request,
                   send_file)
from PIL import Image

app = Flask(
    __name__,
    static_folder="../static",
    template_folder="../templates"
)

UPLOAD_FOLDER = "/tmp"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


def encode_base64(image_to_encode: str | Path,
                  encoded_text: str | Path = Path(__file__).with_suffix(".txt")) -> None:
    """
    Encode the input image as a Base64 string.
    """
    with open(image_to_encode, "rb") as image_file:
        encoded_string = b64encode(image_file.read()).decode("utf-8")
        with open(encoded_text, "w", encoding="utf-8") as text_file:
            text_file.write(encoded_string)


def decode_base64(encoded_text: str | Path,
                  decoded_image: str | Path = Path(__file__).with_suffix(".png")) -> None:
    """
    Decode the input Base64 string into an image.
    """
    with open(encoded_text, "r", encoding="utf-8") as text_file:
        decoded_output = b64decode(text_file.read())
        with open(decoded_image, "wb") as image_file:
            image_file.write(decoded_output)


def shuffle_pixels(origin_image: str | Path,
                   shuffled_image: str | Path,
                   seed: int | None = None,
                   index_file: str | Path | None = Path(__file__).with_suffix(".npz"),
                   image_quality: str = "high") -> None:
    """
    Shuffle the arrangement of pixels.
    """
    scale_of_image_quality = {
        "low": 30,
        "medium": 75,
        "high": 95
    }

    rng = np.random.default_rng(seed)

    pixel_array = np.array(Image.open(origin_image))
    image_size = pixel_array.shape
    flat_pixels = pixel_array.reshape(-1, image_size[2])
    pixel_indices = np.arange(flat_pixels.shape[0])

    rng.shuffle(pixel_indices)

    if seed is None and index_file is not None:
        np.savez_compressed(
            index_file,
            pixel_indices=pixel_indices,
            image_size=image_size
        )

    shuffled_output = Image.fromarray(
        flat_pixels[pixel_indices].reshape(image_size)
    )
    shuffled_output.save(
        shuffled_image,
        quality=scale_of_image_quality[image_quality],
        optimize=True,
        progressive=True,
        compress_level=9
    )


def recover_pixels(shuffled_image: str | Path,
                   recovered_image: str | Path,
                   seed: int | None = None,
                   index_file: str | Path | None = Path(__file__).with_suffix(".npz"),
                   image_quality: str = "high") -> None:
    """
    Recover the arrangement of pixels.
    """
    scale_of_image_quality = {
        "low": 30,
        "medium": 75,
        "high": 95
    }

    pixel_array = np.array(Image.open(shuffled_image))
    image_size = pixel_array.shape
    flat_pixels = pixel_array.reshape(-1, image_size[2])

    if seed is not None and index_file is None:
        rng = np.random.default_rng(seed)
        pixel_indices = np.arange(flat_pixels.shape[0])
        rng.shuffle(pixel_indices)
    elif seed is None and index_file is not None:
        indices_data = np.load(index_file)
        pixel_indices = indices_data["pixel_indices"]
        image_size = tuple(indices_data["image_size"])

    recovered_indices = np.argsort(pixel_indices)

    recovered_output = Image.fromarray(
        flat_pixels[recovered_indices].reshape(image_size)
    )
    recovered_output.save(
        recovered_image,
        quality=scale_of_image_quality[image_quality],
        optimize=True,
        progressive=True,
        compress_level=9
    )


def generate_secure_seed(method: str = "os",
                         passphrase: str | None = None) -> int:
    """
    Generate a secure 128-bit random seed.
    """
    match method:
        case "os":
            return int.from_bytes(os.urandom(16), "big")

        case "secrets":
            return secrets.randbits(128)

        case "hash":
            if passphrase is None:
                raise ValueError(
                    'The "hash" method requires a non-empty passphrase string.'
                )
            hash_hex = hashlib.sha256(passphrase.encode("utf-8")).hexdigest()
            return int(hash_hex, 16) % (2**128)

        case _:
            raise ValueError(
                'Unsupported method. '
                'Choose from "os", "secrets", or "hash".'
            )


@app.route("/")
def index() -> str:
    """
    __doc__
    """
    return render_template("index.html")


@app.route("/encode", methods=["POST"])
def encode() -> Response:
    """
    __doc__
    """
    image_to_encode = request.files["image_to_encode"]
    upload_file_path = Path(UPLOAD_FOLDER) / image_to_encode.filename
    image_to_encode.save(upload_file_path)

    encoded_file_name = (
        f"{Path(image_to_encode.filename).stem}"
        "_encoded"
        f"{Path(image_to_encode.filename).suffix}"
    )
    download_path = Path(UPLOAD_FOLDER) / encoded_file_name

    encode_base64(upload_file_path, download_path)

    response = make_response(send_file(download_path))
    response.headers["Content-Disposition"] = f"attachment; filename={encoded_file_name}"
    return response


@app.route("/decode", methods=["POST"])
def decode() -> Response:
    """
    __doc__
    """
    encoded_text = request.files["encoded_text"]
    upload_file_path = Path(UPLOAD_FOLDER) / encoded_text.filename
    encoded_text.save(upload_file_path)

    decoded_file_name = (
        f"{Path(encoded_text.filename).stem}"
        "_decoded"
        f"{Path(encoded_text.filename).suffix}"
    )
    download_path = Path(UPLOAD_FOLDER) / decoded_file_name

    decode_base64(upload_file_path, download_path)

    response = make_response(send_file(download_path))
    response.headers["Content-Disposition"] = f"attachment; filename={decoded_file_name}"
    return response


@app.route("/shuffle", methods=["POST"])
def shuffle() -> Response:
    """
    __doc__
    """
    original_image = request.files["origin_image"]
    upload_file_path = Path(UPLOAD_FOLDER) / original_image.filename
    original_image.save(upload_file_path)

    shuffled_file_name = (
        f"{Path(original_image.filename).stem}"
        "_shuffled"
        f"{Path(original_image.filename).suffix}"
    )
    download_path = Path(UPLOAD_FOLDER) / shuffled_file_name

    seed_str = request.form.get("seed")
    seed = int(seed_str) if seed_str else None
    index_file = Path(UPLOAD_FOLDER) / "indices.npz" if seed is None else None
    image_quality = request.form.get("image_quality")

    shuffle_pixels(upload_file_path, download_path, seed, index_file, image_quality)

    response = make_response(send_file(download_path))
    response.headers["Content-Disposition"] = f"attachment; filename={shuffled_file_name}"
    return response


@app.route("/recover", methods=["POST"])
def recover() -> Response:
    """
    __doc__
    """
    shuffled_image = request.files["shuffled_image"]
    upload_file_path = Path(UPLOAD_FOLDER) / shuffled_image.filename
    shuffled_image.save(upload_file_path)

    recovered_file_name = (
        f"{Path(shuffled_image.filename).stem}"
        "_recovered"
        f"{Path(shuffled_image.filename).suffix}"
    )
    download_path = Path(UPLOAD_FOLDER) / recovered_file_name

    seed_str = request.form.get("seed")
    seed = int(seed_str) if seed_str else None
    index_file = Path(UPLOAD_FOLDER) / "indices.npz" if seed is None else None
    image_quality = request.form.get("image_quality")

    recover_pixels(upload_file_path, download_path, seed, index_file, image_quality)

    response = make_response(send_file(download_path))
    response.headers["Content-Disposition"] = f"attachment; filename={recovered_file_name}"
    return response


if __name__ == "__main__":

    app.run()
