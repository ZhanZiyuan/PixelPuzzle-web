#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
https://github.com/google/material-design-lite

https://geek-docs.com/flask/flask-questions/396_flask_how_to_connect_backend_python_flask_with_frontend_html_css_javascript.html

https://blog.csdn.net/u011035397/article/details/103583205

https://tutorial.helloflask.com/static/

https://qiita.com/mink0212/items/a4eb875f19b0e47718d3
"""

import tempfile
from base64 import b64decode, b64encode
from pathlib import Path
from typing import Union

import flask
import numpy as np
from flask import Flask, make_response, render_template, request, send_file
from PIL import Image

app = Flask(__name__)


def encode_base64(image_to_encode: str,
                  encoded_text: Union[str, Path] = Path(__file__).with_suffix(".txt")) -> None:
    """
    Encode the input image as a Base64 string.
    """
    with open(image_to_encode, "rb") as image_file:
        encoded_string = b64encode(image_file.read()).decode("utf-8")
        with open(encoded_text, "w", encoding="utf-8") as text_file:
            text_file.write(encoded_string)


def decode_base64(encoded_text: str,
                  decoded_image: Union[str, Path] = Path(__file__).with_suffix(".png")) -> None:
    """
    Decode the input Base64 string into an image.
    """
    with open(encoded_text, "r", encoding="utf-8") as text_file:
        decoded_output = b64decode(text_file.read())
        with open(decoded_image, "wb") as image_file:
            image_file.write(decoded_output)


def shuffle_pixels(origin_image: str,
                   shuffled_image: str,
                   seed: Union[int, None] = None,
                   index_file: Union[str, Path, None] = Path(__file__).with_suffix(".npz"),
                   image_quality: str = "high") -> None:
    """
    Shuffle the arrangement of pixels on two dimensions.
    """
    scale_of_image_quality = {
        "low": 30,
        "medium": 75,
        "high": 95
    }

    rng = np.random.default_rng(seed)

    pixel_array = np.array(
        Image.open(origin_image)
    )
    indices_shuffled_x = rng.permutation(pixel_array.shape[0])
    indices_shuffled_y = rng.permutation(pixel_array.shape[1])

    if seed is None and index_file is not None:
        np.savez(
            index_file,
            indices_shuffled_x=indices_shuffled_x,
            indices_shuffled_y=indices_shuffled_y
        )

    shuffled_output = Image.fromarray(
        pixel_array[indices_shuffled_x[:, np.newaxis], indices_shuffled_y, :]
    )
    shuffled_output.save(
        shuffled_image,
        quality=scale_of_image_quality[image_quality],
        optimize=True,
        progressive=True,
        compress_level=9
    )


def recover_pixels(shuffled_image: str,
                   recovered_image: str,
                   seed: Union[int, None] = None,
                   index_file: Union[str, Path, None] = Path(__file__).with_suffix(".npz"),
                   image_quality: str = "high") -> None:
    """
    Recover the arrangement of pixels on two dimensions.
    """
    scale_of_image_quality = {
        "low": 30,
        "medium": 75,
        "high": 95
    }

    pixel_array = np.array(
        Image.open(shuffled_image)
    )

    if seed is not None and index_file is None:
        rng = np.random.default_rng(seed)
        indices_shuffled_x = rng.permutation(pixel_array.shape[0])
        indices_shuffled_y = rng.permutation(pixel_array.shape[1])
    elif seed is None and index_file is not None:
        indices_data = np.load(index_file)
        indices_shuffled_x = indices_data["indices_shuffled_x"]
        indices_shuffled_y = indices_data["indices_shuffled_y"]

    indices_recovered_x = np.argsort(indices_shuffled_x)
    indices_recovered_y = np.argsort(indices_shuffled_y)

    recovered_output = Image.fromarray(
        pixel_array[indices_recovered_x[:, np.newaxis], indices_recovered_y, :]
    )
    recovered_output.save(
        recovered_image,
        quality=scale_of_image_quality[image_quality],
        optimize=True,
        progressive=True,
        compress_level=9
    )


def cleanup_temp_files(file_paths: list) -> None:
    """
    __doc__
    """
    for file_path in file_paths:
        Path(file_path).unlink()


@app.route("/")
def index() -> str:
    """
    __doc__
    """
    return render_template("index.html")


@app.route("/encode", methods=["POST"])
def encode() -> flask.Response:
    """
    __doc__
    """
    image_to_encode = request.files["image_to_encode"]
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        image_to_encode.save(temp_file.name)
        encoded_text = temp_file.name + ".txt"
        encode_base64(temp_file.name, encoded_text)
        response = make_response(send_file(encoded_text))
        response.headers["Content-Disposition"] = "inline; filename=encoded.txt"
    cleanup_temp_files([temp_file.name, encoded_text])
    return response


@app.route("/decode", methods=["POST"])
def decode() -> flask.Response:
    """
    __doc__
    """
    encoded_text = request.files["encoded_text"]
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        encoded_text.save(temp_file.name)
        decoded_image = temp_file.name + ".png"
        decode_base64(temp_file.name, decoded_image)
        response = make_response(send_file(decoded_image))
        response.headers["Content-Disposition"] = "inline; filename=decoded.png"
    # cleanup_temp_files([temp_file.name, decoded_image])
    return response


@app.route("/shuffle", methods=["POST"])
def shuffle() -> flask.Response:
    """
    __doc__
    """
    origin_image = request.files["origin_image"]
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        origin_image.save(temp_file.name)
        shuffled_image = temp_file.name + ".png"
        seed = request.form.get("seed")
        seed = None if seed == "no" else int(seed)
        index_file = temp_file.name + ".npz" if seed is None else None
        image_quality = request.form.get("image_quality")
        shuffle_pixels(temp_file.name, shuffled_image, seed, index_file, image_quality)
        response = make_response(send_file(shuffled_image))
        response.headers["Content-Disposition"] = "inline; filename=shuffled.png"
    file_paths = [temp_file.name, shuffled_image]
    if index_file:
        file_paths.append(index_file)
    # cleanup_temp_files(file_paths)
    return response


@app.route("/recover", methods=["POST"])
def recover() -> flask.Response:
    """
    __doc__
    """
    shuffled_image = request.files["shuffled_image"]
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        shuffled_image.save(temp_file.name)
        recovered_image = temp_file.name + ".png"
        seed = request.form.get("seed")
        seed = None if seed == "no" else int(seed)
        index_file = temp_file.name + ".npz" if seed is None else None
        image_quality = request.form.get("image_quality")
        recover_pixels(temp_file.name, recovered_image, seed, index_file, image_quality)
        response = make_response(send_file(recovered_image))
        response.headers["Content-Disposition"] = "inline; filename=recovered.png"
    file_paths = [temp_file.name, recovered_image]
    if index_file:
        file_paths.append(index_file)
    # cleanup_temp_files(file_paths)
    return response


if __name__ == "__main__":

    app.run(debug=True)
