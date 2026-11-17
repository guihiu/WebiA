from flask import Flask, redirect, render_template, request, session, url_for

from locales import LOCALES


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY="local-development-only",
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )
    if test_config:
        app.config.update(test_config)

    supported_locales = ("pt", "en", "es")

    @app.before_request
    def ensure_locale():
        locale = request.args.get("lang")
        if locale in supported_locales:
            session["locale"] = locale
        elif "locale" not in session:
            session["locale"] = "pt"

    @app.context_processor
    def template_globals():
        locale = session.get("locale", "pt")
        if locale not in supported_locales:
            locale = "pt"
        return {
            "locale": locale,
            "text": LOCALES[locale],
            "supported_locales": supported_locales,
        }

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/mlp")
    def mlp():
        return render_template("mlp.html")

    @app.route("/rbf")
    def rbf():
        return render_template("rbf.html")

    @app.route("/mlp-training")
    def mlp_training():
        return render_template("mlp_training.html")

    @app.route("/rbf-training")
    def rbf_training():
        return render_template("rbf_training.html")

    @app.route("/training-data")
    def training_data():
        return render_template("training_data.html")

    @app.route("/set-language/<locale>")
    def set_language(locale):
        if locale not in supported_locales:
            locale = "pt"
        session["locale"] = locale
        next_page = request.args.get("next")
        if next_page not in (
            "/",
            "/mlp",
            "/rbf",
            "/mlp-training",
            "/rbf-training",
            "/training-data",
        ):
            next_page = "/"
        return redirect(next_page)

    @app.errorhandler(404)
    def not_found(error):
        locale = session.get("locale", "pt")
        if locale not in supported_locales:
            locale = "pt"
        return render_template("404.html", text=LOCALES[locale]), 404

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
