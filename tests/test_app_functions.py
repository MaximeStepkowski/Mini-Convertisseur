import os
import pytest
import requests
from unittest.mock import MagicMock, mock_open, patch

from app_functions import (
    API_KEY_ENV_VAR,
    CurrencyRateError,
    convert,
    get_api_key,
    get_rates,
)

RATES = {"EUR": 1.0, "USD": 1.1, "GBP": 0.86, "JPY": 130.0}


# ---------------------------------------------------------------------------
# convert()
# ---------------------------------------------------------------------------

class TestConvert:
    def test_conversion_normale(self):
        result = convert(100.0, "EUR", "USD", RATES)
        assert result == pytest.approx(110.0)

    def test_conversion_inverse(self):
        result = convert(110.0, "USD", "EUR", RATES)
        assert result == pytest.approx(100.0)

    def test_montant_zero_leve_value_error(self):
        with pytest.raises(ValueError, match="strictement positif"):
            convert(0.0, "EUR", "USD", RATES)

    def test_montant_negatif_leve_value_error(self):
        with pytest.raises(ValueError, match="strictement positif"):
            convert(-10.0, "EUR", "USD", RATES)

    def test_devises_identiques_leve_value_error(self):
        with pytest.raises(ValueError, match="différentes"):
            convert(100.0, "USD", "USD", RATES)

    def test_devise_source_inconnue_leve_currency_rate_error(self):
        with pytest.raises(CurrencyRateError, match="introuvable"):
            convert(100.0, "XYZ", "EUR", RATES)

    def test_devise_cible_inconnue_leve_currency_rate_error(self):
        with pytest.raises(CurrencyRateError, match="introuvable"):
            convert(100.0, "EUR", "XYZ", RATES)

    def test_taux_vide_leve_currency_rate_error(self):
        with pytest.raises(CurrencyRateError):
            convert(100.0, "EUR", "USD", {})


# ---------------------------------------------------------------------------
# get_api_key()
# ---------------------------------------------------------------------------

class TestGetApiKey:
    def test_retourne_cle_depuis_variable_env(self):
        with patch.dict(os.environ, {API_KEY_ENV_VAR: "ma_cle_test"}):
            assert get_api_key() == "ma_cle_test"

    def test_retourne_cle_depuis_fichier_env(self, tmp_path, monkeypatch):
        env_file = tmp_path / ".env"
        env_file.write_text(f"{API_KEY_ENV_VAR}=cle_depuis_fichier\n")
        monkeypatch.delenv(API_KEY_ENV_VAR, raising=False)
        monkeypatch.chdir(tmp_path)
        assert get_api_key() == "cle_depuis_fichier"

    def test_ignore_les_autres_lignes_du_fichier_env(self, tmp_path, monkeypatch):
        env_file = tmp_path / ".env"
        env_file.write_text("AUTRE_VAR=valeur\n" + f"{API_KEY_ENV_VAR}=bonne_cle\n")
        monkeypatch.delenv(API_KEY_ENV_VAR, raising=False)
        monkeypatch.chdir(tmp_path)
        assert get_api_key() == "bonne_cle"

    def test_supprime_les_guillemets_autour_de_la_valeur(self, tmp_path, monkeypatch):
        env_file = tmp_path / ".env"
        env_file.write_text(f'{API_KEY_ENV_VAR}="cle_avec_guillemets"\n')
        monkeypatch.delenv(API_KEY_ENV_VAR, raising=False)
        monkeypatch.chdir(tmp_path)
        assert get_api_key() == "cle_avec_guillemets"

    def test_retourne_none_si_cle_absente_du_fichier_env(self, tmp_path, monkeypatch):
        env_file = tmp_path / ".env"
        env_file.write_text("AUTRE_VAR=valeur\n")
        monkeypatch.delenv(API_KEY_ENV_VAR, raising=False)
        monkeypatch.chdir(tmp_path)
        assert get_api_key() is None

    def test_retourne_none_si_pas_de_fichier_env(self, tmp_path, monkeypatch):
        monkeypatch.delenv(API_KEY_ENV_VAR, raising=False)
        monkeypatch.chdir(tmp_path)
        assert get_api_key() is None

    def test_variable_env_prioritaire_sur_fichier(self, tmp_path, monkeypatch):
        env_file = tmp_path / ".env"
        env_file.write_text(f"{API_KEY_ENV_VAR}=cle_fichier\n")
        monkeypatch.chdir(tmp_path)
        with patch.dict(os.environ, {API_KEY_ENV_VAR: "cle_env"}):
            assert get_api_key() == "cle_env"


# ---------------------------------------------------------------------------
# get_rates()
# ---------------------------------------------------------------------------

def _mock_response(json_data=None, raise_for_status=None, raise_exception=None):
    mock = MagicMock()
    if raise_exception:
        mock.side_effect = raise_exception
    else:
        if raise_for_status:
            mock.return_value.raise_for_status.side_effect = raise_for_status
        else:
            mock.return_value.raise_for_status.return_value = None
        mock.return_value.json.return_value = json_data
    return mock


class TestGetRates:
    def test_succes_retourne_les_taux(self):
        payload = {"result": "success", "conversion_rates": {"EUR": 1.0, "USD": 1.1}}
        with patch("app_functions.requests.get", _mock_response(json_data=payload)):
            rates = get_rates(api_key="cle_test")
        assert rates == {"EUR": 1.0, "USD": 1.1}

    def test_sans_cle_leve_currency_rate_error(self):
        with patch("app_functions.get_api_key", return_value=None):
            with pytest.raises(CurrencyRateError, match="Clé API manquante"):
                get_rates()

    def test_erreur_http_leve_currency_rate_error(self):
        with patch(
            "app_functions.requests.get",
            _mock_response(raise_for_status=requests.HTTPError("404")),
        ):
            with pytest.raises(CurrencyRateError, match="Impossible de récupérer"):
                get_rates(api_key="cle_test")

    def test_erreur_reseau_leve_currency_rate_error(self):
        mock_get = MagicMock(side_effect=requests.ConnectionError())
        with patch("app_functions.requests.get", mock_get):
            with pytest.raises(CurrencyRateError, match="Impossible de récupérer"):
                get_rates(api_key="cle_test")

    def test_json_invalide_leve_currency_rate_error(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.side_effect = ValueError("json invalide")
        with patch("app_functions.requests.get", return_value=mock_resp):
            with pytest.raises(CurrencyRateError, match="Réponse invalide"):
                get_rates(api_key="cle_test")

    def test_api_result_echec_leve_currency_rate_error(self):
        payload = {"result": "error", "error-type": "invalid-key"}
        with patch("app_functions.requests.get", _mock_response(json_data=payload)):
            with pytest.raises(CurrencyRateError, match="invalid-key"):
                get_rates(api_key="cle_test")

    def test_api_result_echec_sans_type_erreur(self):
        payload = {"result": "error"}
        with patch("app_functions.requests.get", _mock_response(json_data=payload)):
            with pytest.raises(CurrencyRateError, match="erreur inconnue"):
                get_rates(api_key="cle_test")

    def test_conversion_rates_absent_leve_currency_rate_error(self):
        payload = {"result": "success"}
        with patch("app_functions.requests.get", _mock_response(json_data=payload)):
            with pytest.raises(CurrencyRateError, match="absents de la réponse"):
                get_rates(api_key="cle_test")

    def test_conversion_rates_non_dict_leve_currency_rate_error(self):
        payload = {"result": "success", "conversion_rates": "pas_un_dict"}
        with patch("app_functions.requests.get", _mock_response(json_data=payload)):
            with pytest.raises(CurrencyRateError, match="absents de la réponse"):
                get_rates(api_key="cle_test")

    def test_utilise_get_api_key_si_cle_non_fournie(self):
        payload = {"result": "success", "conversion_rates": {"EUR": 1.0}}
        with patch("app_functions.get_api_key", return_value="cle_auto") as mock_key:
            with patch("app_functions.requests.get", _mock_response(json_data=payload)):
                get_rates()
        mock_key.assert_called_once()

    def test_devise_de_base_dans_url(self):
        payload = {"result": "success", "conversion_rates": {"EUR": 1.0}}
        with patch("app_functions.requests.get", _mock_response(json_data=payload)) as mock_get:
            get_rates(base_currency="USD", api_key="cle_test")
        url_appellee = mock_get.call_args[0][0]
        assert "USD" in url_appellee
