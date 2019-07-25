import math

# Подсчет цены за отправку
def calc_price(sheet_result, req_weight, shipping_method, is_ems):
    values = sheet_result.get('values', [])
    if not values:
        print('No data found.')
    else:
        weight = 0
        if req_weight == 0.3:
            weight = req_weight
        else:
            weight = math.ceil(req_weight * 2) / 2
        # Проверка на значение > 10 и выявление этого остатка
        remainder = 0
        if weight > 10:
            remainder = math.ceil(weight - 10)
            if remainder > 0 and remainder < 1:
                remainder = 200
            else:
                remainder = remainder * 200
            weight = '10.0'
        else:
            weight = str(weight)
            price = 0
        for row in values:
            if(row[0] == weight):
                price = int(row[shipping_method])
        
        return price + remainder