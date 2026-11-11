import json
import logging
from pathlib import Path

import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

BASE = Path(__file__).parent
ARQUIVO_PAINEL = BASE / "static" / "dashboard.html"
ARQUIVO_DADOS = BASE / "data" / "dados.json"


@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )


# ---------------------------------------------------------------------------
# Funções do projeto TAPRA6ANKAIOHN (Kaio H. Natal, Alex Allan, Gustavo Alexandre)
# ---------------------------------------------------------------------------

@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
def timer_trigger_teste1(myTimer: func.TimerRequest) -> None:
    """Roda a cada minuto (precisa de AzureWebJobsStorage configurado)."""
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')


def _responder_ola(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    return func.HttpResponse(
        "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
        status_code=200
    )


@app.route(route="http_trigger_teste1", auth_level=func.AuthLevel.ANONYMOUS)
def http_trigger_teste1(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    return _responder_ola(req)


@app.route(route="http_trigger_Hello", auth_level=func.AuthLevel.ANONYMOUS)
def http_trigger_Hello(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    return _responder_ola(req)


@app.route(route="dashboard", methods=["GET"])
def dashboard(req: func.HttpRequest) -> func.HttpResponse:
    """Painel executivo de receita (HTML). Abre em /api/dashboard."""
    html = ARQUIVO_PAINEL.read_text(encoding="utf-8")
    return func.HttpResponse(html, mimetype="text/html", charset="utf-8")


@app.route(route="dados", methods=["GET"])
def dados(req: func.HttpRequest) -> func.HttpResponse:
    """Dados (fictícios) do painel em JSON. Filtro opcional: /api/dados?regiao=Sul"""
    conteudo = json.loads(ARQUIVO_DADOS.read_text(encoding="utf-8"))

    regiao = req.params.get("regiao")
    if regiao:
        if regiao not in conteudo["series"]:
            return func.HttpResponse(
                json.dumps(
                    {"erro": f"Região inválida: {regiao}", "validas": conteudo["regioes"]},
                    ensure_ascii=False,
                ),
                mimetype="application/json",
                status_code=400,
            )
        conteudo["regioes"] = [regiao]
        conteudo["series"] = {regiao: conteudo["series"][regiao]}

    return func.HttpResponse(
        json.dumps(conteudo, ensure_ascii=False),
        mimetype="application/json",
        charset="utf-8",
    )
