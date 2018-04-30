import json
from datetime import datetime, date

def assign_data_to_fieldnames(result):
    rows = []
    rows_json = []
    response = {}

    if not type(result) is list:
        rows.append(result)
    else:
        rows = result

    result_fields = result[0].keys()

    for row in rows:
        row_object = {}
        for i in range(len(result_fields)):
            if isinstance(row[i], (datetime, date)):
                row_object[result_fields[i]] = row[i].isoformat()
            else:
                row_object[result_fields[i]] = row[i]

        rows_json.append({ 'place': row_object })

    response['places'] = rows_json
    return json.dumps(response)
