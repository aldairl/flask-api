import os
import pandas as pd

def proccess_custom_template(df):
    df = df.fillna('')
    df = df.drop([0])
    
    return df


def format_data_df(df):
    df_dict = df.to_dict(orient='list')
    
    df_columns = df.columns.to_list()
    
    data = [
            { "key": index, **{ column: df_dict[column][index] for i, column in enumerate(df_columns) } }
            for index in range(len(df))
        ]

    return data


def format_columns_df(df):
    df_columns = df.columns.to_list()
    
    columns = [ 
            { "title": column, "dataIndex": column, "key": column, "editable": True,}
            for column in df_columns
        ]
    
    return columns


def save_excel_file(path_folder, filename, excel_file):
    try:
        
        # Verificar si el directorio existe; si no, crearlo
        if not os.path.exists(path_folder):
            os.makedirs(path_folder)
        
        pathFile = os.path.join(path_folder, '..', 'temp', filename)

        with pd.ExcelWriter(pathFile, engine='openpyxl') as writer:
            for sheet_name in excel_file.sheet_names:
                df = excel_file.parse(sheet_name)
                df.to_excel(writer, index=False, sheet_name=sheet_name)
        
        return True
    except Exception as e:
        print(e)
        return False

