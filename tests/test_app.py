import json

import pytest

from app import create_app


@pytest.fixture()
def client(tmp_path):
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-only",
        "CONFIG_OUTPUT_DIR": str(tmp_path),
    })
    return app.test_client()


@pytest.mark.parametrize(
    "path",
    ["/", "/mlp", "/rbf", "/mlp-training", "/rbf-training", "/training-data"],
)
def test_public_routes(client, path):
    response = client.get(path)
    assert response.status_code == 200
    assert b"<main" in response.data


def test_training_pages_render_configuration_controls(client):
    mlp_response = client.get("/mlp-training")
    rbf_response = client.get("/rbf-training")

    assert b'data-mlp-config' in mlp_response.data
    assert b'data-hidden-layer-count' in mlp_response.data
    assert b'data-layer-activation' in mlp_response.data
    assert b'data-activation-template' in mlp_response.data
    assert b'data-rbf-config' in rbf_response.data
    assert b'data-radial-units' in rbf_response.data
    assert b'data-save-url="/save-configuration/mlp"' in mlp_response.data
    assert b'data-save-url="/save-configuration/rbf"' in rbf_response.data


def test_saving_mlp_configuration_writes_json_file(client, tmp_path):
    configuration = {
        "hidden_layers": [
            {"neurons": 24, "activation": "tanh"},
            {"neurons": 8, "activation": "relu"},
        ],
    }

    response = client.post("/save-configuration/mlp", json=configuration)

    assert response.status_code == 200
    assert response.json == {"filename": "mlp.json"}
    assert json.loads(
        (tmp_path / "mlp.json").read_text(encoding="utf-8")
    ) == configuration


def test_saving_rbf_configuration_writes_json_file(client, tmp_path):
    configuration = {
        "radial_units": 32,
        "spread": 0.75,
        "activation": "sigmoid",
    }

    response = client.post("/save-configuration/rbf", json=configuration)

    assert response.status_code == 200
    assert response.json == {"filename": "rbf.json"}
    assert json.loads(
        (tmp_path / "rbf.json").read_text(encoding="utf-8")
    ) == configuration


def test_invalid_configuration_is_not_saved(client, tmp_path):
    response = client.post(
        "/save-configuration/mlp",
        json={"hidden_layers": [{"neurons": 0, "activation": "relu"}]},
    )

    assert response.status_code == 400
    assert not (tmp_path / "mlp.json").exists()


def test_training_data_page_accepts_csv_and_offers_page_sizes(client):
    response = client.get("/training-data")

    assert response.status_code == 200
    assert b'accept=".csv,text/csv"' in response.data
    assert b'data-drop-zone' in response.data
    assert b'<option value="10">10</option>' in response.data
    assert b'<option value="20">20</option>' in response.data
    assert b'<option value="50">50</option>' in response.data


@pytest.mark.parametrize(
    ("locale", "expected"),
    [
        ("pt", "Perceptron Multicamadas"),
        ("en", "Multilayer Perceptron"),
        ("es", "Perceptrón multicapa"),
    ],
)
def test_locale_switching(client, locale, expected):
    response = client.get(f"/set-language/{locale}?next=/mlp", follow_redirects=True)
    assert response.status_code == 200
    assert expected.encode("utf-8") in response.data


def test_invalid_locale_falls_back_to_portuguese(client):
    response = client.get("/set-language/fr?next=/", follow_redirects=True)
    assert response.status_code == 200
    assert "MLP x RBF".encode() in response.data


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("/mlp-training", "Configuración de entrenamiento MLP"),
        ("/rbf-training", "Configuración de entrenamiento RBF"),
    ],
)
def test_language_switch_returns_to_training_page(client, path, expected):
    response = client.get(f"/set-language/es?next={path}", follow_redirects=True)
    assert response.status_code == 200
    assert expected.encode("utf-8") in response.data


def test_unknown_route_returns_404(client):
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    assert b"404" in response.data
