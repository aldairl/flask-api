from flask import Blueprint, request
from .controllers import health_check, filter_by_date, upload_file


main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET"])
def health():
    """Health check endpoint"""
    return health_check()


@main_bp.route("/data", methods=["POST"])
def get_data():
    """Endpoint para recibir filtros por fecha"""
    data = request.get_json()
    return filter_by_date(data)


@main_bp.route("/upload", methods=["POST"])
def upload():
    """Endpoint para recibir archivo"""
    file = request.files['file']
    
    return upload_file(file)