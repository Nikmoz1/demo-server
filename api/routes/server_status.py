from typing import Dict
from http import HTTPStatus
from flask_restx import Namespace, Resource

server_status_ns = Namespace("server-status", description="Check status server")


@server_status_ns.doc("")
@server_status_ns.route("/check")
class CheckStatus(Resource):

    @server_status_ns.response(int(HTTPStatus.OK), "OK")
    def get(self) -> Dict[str, HTTPStatus]:
        return {"status_code": HTTPStatus.OK}
