import lib
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)
KAZPOST_SPREADSHEET_ID = "" #ID in GOOGLESHEETS
# ROUTER
@app.route('/')
def main():
    return 'Service work'


@app.route('/shipping_calc', methods=['POST'])
@cross_origin(supports_credentials=True)
def shipping_calc():
    data = request.get_json()
    try:
        if(type(data["weight"]) is float or type(data["weight"]) is int):
            SPREADSHEET_NAME = ''
            req_country = data["country"]
            req_weight = data["weight"]
            shipping_method = data["shipping_method"]
            is_ems = data["is_ems"]
            # Направление в правильную таблицу
            if req_country == 8 and not shipping_method == "abroad":
                SPREADSHEET_NAME = 'in_kz!A3:D'
            elif req_country == 8 and shipping_method == "abroad":
                SPREADSHEET_NAME = 'in_kz_ground!A2:D'
            elif req_country == 7 and not is_ems:
                SPREADSHEET_NAME = 'from_kz_to_ru!A2:D'
            elif req_country == 7 and is_ems:
                SPREADSHEET_NAME = 'from_kz_to_ru_fast!A2:C'
            elif req_country < 7 and not is_ems:
                SPREADSHEET_NAME = 'from_kz_abroad!A2:G'
            elif req_country < 7 and  is_ems:
                SPREADSHEET_NAME = 'from_kz_abroad_fast!A2:G'
            
            # ТЕСТ ИДЕТ
            price = SPREADSHEET_NAME;
            # sheet = lib.auth().spreadsheets()
            # sheet_result = sheet.values().get(spreadsheetId=KAZPOST_SPREADSHEET_ID,
            #                     range=SPREADSHEET_NAME).execute()
            # price = lib.calc_price(sheet_result, req_weight, shipping_method, is_ems)
            return jsonify({"shipping_price": price}), 200
        else:
            return jsonify({"error": "Invalid data"}), 400

    except Exception as err:
        print("Error: %s" % err)
        return ({"error": err}), 400


@app.route('/getCountry', methods=['GET'])
def get_country():
    try: 
        sheet = lib.auth().spreadsheets()
        result = sheet.values().get(spreadsheetId=KAZPOST_SPREADSHEET_ID,
                                range='country_list!A2:B').execute()
        values = result.get('values', [])
        country = []
        if not values:
            print('No data found.')
        else:
            for row in values:
                country.append({
                    "name": row[0],
                    "value": int(row[1])
                })
            country.sort(key=lambda x: x["name"])
            return jsonify({"country": country})
    except Exception as err:
        print("Error: %s" % err)
        return jsonify({"error": err}), 400


if __name__ == '__main__':
    app.run(debug=True)
