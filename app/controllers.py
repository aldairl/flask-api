from flask import jsonify
from datetime import datetime
import pandas as pd
import io
import os

from .utils import format_data_df, proccess_custom_template, format_columns_df, save_excel_file

def health_check():
    """Verifica el estado de la aplicación."""
    return jsonify({"status": "ok", "message": "API is healthy!"}), 200


def filter_by_date(data):
    """Filtra resultados según las fechas proporcionadas."""
    try:
        start_date = datetime.strptime(data.get("start_date"), "%Y-%m-%d")
        end_date = datetime.strptime(data.get("end_date"), "%Y-%m-%d")

        # Aquí puedes añadir tu lógica para filtrar datos.
        # Por ahora solo devolvemos las fechas recibidas.
        if start_date > end_date:
            return jsonify({"error": "start_date cannot be after end_date"}), 400
        
        return jsonify({
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "message": "Dates received successfully!"
        }), 200

    except (ValueError, TypeError):
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
    
def upload_file(file):
    try:
        excel_data = io.BytesIO(file.read())
        df = pd.read_excel(excel_data, header=1)
        
        df = proccess_custom_template(df)
        
        data = format_data_df(df)
        columns = format_columns_df(df)
        
        excel_file = pd.ExcelFile(file)
        sheets = [ { "label": name, "value": name } for name in excel_file.sheet_names]
        
        # save file
        filename = file.filename.replace(' ', '_')
        current_folder = os.path.abspath(os.path.dirname(__file__))
        path_folder = os.path.join(current_folder, '..', 'temp')
        save_excel_file(path_folder, filename, excel_file)
        
        body = {
            "columns": columns,
            "data": data,
            "sheets": sheets,
            "filename": filename
        }
        
        return jsonify(body), 200
    except Exception as e:
        return jsonify({"error": f"Failed to process the file :/: {str(e)}"}), 500

