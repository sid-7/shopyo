import os
import json

from flask import current_app
from flask import send_from_directory
from flask import Blueprint

# from flask import render_template
# from flask import url_for
# from flask import redirect
# from flask import flash
# from flask import request

# from shopyoapi.enhance import base_context
# from shopyoapi.html import notify_success
# from shopyoapi.forms import flash_errors

from shopyoapi.enhance import get_setting

dirpath = os.path.dirname(os.path.abspath(__file__))
module_info = {}

with open(dirpath + "/info.json") as f:
    module_info = json.load(f)

globals()["{}_blueprint".format(module_info["module_name"])] = Blueprint(
    "{}".format(module_info["module_name"]),
    __name__,
    template_folder="templates",
    url_prefix=module_info["url_prefix"],
)


module_blueprint = globals()["{}_blueprint".format(module_info["module_name"])]


@module_blueprint.route("/")
def index():
    return module_info["display_string"]


@module_blueprint.route("/theme/active/styles.css")
def active_theme_css():
    theme_dir = os.path.join(
        current_app.config["BASE_DIR"], "themes", get_setting("ACTIVE_THEME")
    )
    # return theme_dir
    return send_from_directory(theme_dir, "styles.css")
