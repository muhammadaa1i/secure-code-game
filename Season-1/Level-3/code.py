# Welcome to Secure Code Game Season-1/Level-3!

# You know how to play by now, good luck!

import os
from flask import Flask, request

### Unrelated to the exercise -- Starts here -- Please ignore
app = Flask(__name__)
@app.route("/")
def source():
    TaxPayer('foo', 'bar').get_tax_form_attachment(request.args["input"])
    TaxPayer('foo', 'bar').get_prof_picture(request.args["input"])
### Unrelated to the exercise -- Ends here -- Please ignore

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def safe_path(path):
    # Resolves the full real path (follows '..' and symlinks) and accepts
    # it only when it stays inside BASE_DIR; prefix checks are not enough.
    full = os.path.realpath(os.path.join(BASE_DIR, path))
    if os.path.commonpath([full, BASE_DIR]) != BASE_DIR:
        return None
    return full


class TaxPayer:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.prof_picture = None
        self.tax_form_attachment = None

    # returns the path of an optional profile picture that users can set
    def get_prof_picture(self, path=None):
        # setting a profile picture is optional
        if not path:
            return None

        # defends against path traversal attacks
        prof_picture_path = safe_path(path)
        if prof_picture_path is None:
            return None

        with open(prof_picture_path, 'rb') as pic:
            picture = bytearray(pic.read())

        # assume that image is returned on screen after this
        return prof_picture_path

    # returns the path of an attached tax form that every user should submit
    def get_tax_form_attachment(self, path=None):
        tax_data = None

        if not path:
            raise Exception("Error: Tax form is required for all users")

        # defends against path traversal attacks
        tax_form_path = safe_path(path)
        if tax_form_path is None:
            return None

        with open(tax_form_path, 'rb') as form:
            tax_data = bytearray(form.read())

        # assume that tax data is returned on screen after this
        return tax_form_path