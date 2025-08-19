#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Encode/decode images using Base64
or shuffle/recover the pixels of images.
"""

from pathlib import Path

from flask import (Flask, Response, make_response, render_template, request,
                   send_file)
from pixelpuzzle.core import (decode_base64, encode_base64, recover_pixels,
                              shuffle_pixels)

app = Flask(
    __name__,
    static_folder="../static",
    template_folder="../templates"
)

UPLOAD_FOLDER = "/tmp"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


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

    encoded_file_name = f"{Path(image_to_encode.filename).stem}_encoded.txt"
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

    decoded_file_name = f"{Path(encoded_text.filename).stem}_decoded.png"
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
