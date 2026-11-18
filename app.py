import json
import math
from pathlib import Path

from flask import Flask, redirect, render_template, request, session, url_for

from locales import LOCALES


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY="local-development-only",
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        CONFIG_OUTPUT_DIR=app.root_path,
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

    @app.post("/save-configuration/<network>")
    def save_configuration(network):
        if network not in ("mlp", "rbf"):
            return {"error": "Unsupported network."}, 404

        configuration = request.get_json(silent=True)
        if not isinstance(configuration, dict):
            return {"error": "A JSON configuration is required."}, 400

        if network == "mlp":
            layers = configuration.get("hidden_layers")
            valid = (
                set(configuration) == {"hidden_layers"}
                and isinstance(layers, list)
                and 1 <= len(layers) <= 8
                and all(
                    isinstance(layer, dict)
                    and set(layer) == {"neurons", "activation"}
                    and type(layer["neurons"]) is int
                    and 1 <= layer["neurons"] <= 512
                    and layer["activation"]
                    in ("relu", "tanh", "sigmoid", "softmax", "linear")
                    for layer in layers
                )
            )
        else:
            units = configuration.get("radial_units")
            spread = configuration.get("spread")
            valid = (
                set(configuration) == {"radial_units", "spread", "activation"}
                and type(units) is int
                and 1 <= units <= 512
                and type(spread) in (int, float)
                and math.isfinite(spread)
                and 0.01 <= spread <= 1000
                and configuration["activation"] in ("linear", "sigmoid", "softmax")
            )

        if not valid:
            return {"error": "The configuration contains invalid values."}, 400

        output_path = Path(app.config["CONFIG_OUTPUT_DIR"]) / f"{network}.json"
        try:
            output_path.write_text(
                json.dumps(configuration, indent=2) + "\n",
                encoding="utf-8",
            )
        except OSError:
            app.logger.exception("Could not save %s configuration.", network)
            return {"error": "Could not save the configuration."}, 500

        return {"filename": output_path.name}

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
