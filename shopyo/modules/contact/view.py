from flask import Blueprint
from flask import render_template
from flask import url_for
from flask import redirect
from flask import flash
from flask import request

from .forms import ContactForm
from .models import ContactMessage
from shopyoapi.enhance import base_context

from shopyoapi.html import notify_success


from flask_login import login_required

contact_blueprint = Blueprint(
    "contact",
    __name__,
    url_prefix="/contact",
    template_folder="templates",
)


@contact_blueprint.route("/")
def index():
    context = base_context()
    form = ContactForm()

    context.update({"form": form})
    return render_template("contact/contact_form.html", **context)


@login_required
@contact_blueprint.route("/validate_message", methods=["GET", "POST"])
def validate_message():
    if request.method == "POST":
        form = ContactForm()
        if not form.validate_on_submit():
            flash_errors(form)
            return redirect(url_for("contact.index"))

        name = form.name.data
        email = form.email.data
        message = form.message.data

        contact_message = ContactMessage(name=name, email=email, message=message)
        contact_message.insert()
        flash(notify_success("Message submitted!"))
        return redirect(url_for("contact.index"))


@login_required
@contact_blueprint.route("/dashboard", methods=["GET"], defaults={"page": 1})
@contact_blueprint.route("/dashboard/<int:page>", methods=["GET"])
def dashboard(page):
    context = base_context()

    per_page = 10
    messages = ContactMessage.query.paginate(page, per_page, error_out=False)
    context.update({"messages": messages})
    return render_template("contact/dashboard.html", **context)
