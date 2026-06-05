def calculate_total(items, discount_code, customer_type, is_holiday):
    total = 0
    for item in items:
        if item['category'] == 'electronics':
            if item['price'] > 1000:
                if customer_type == 'premium':
                    if is_holiday:
                        total += item['price'] * 0.7
                    else:
                        total += item['price'] * 0.8
                else:
                    if is_holiday:
                        total += item['price'] * 0.85
                    else:
                        total += item['price'] * 0.9
            else:
                if customer_type == 'premium':
                    total += item['price'] * 0.9
                else:
                    total += item['price'] * 0.95
        elif item['category'] == 'clothing':
            if discount_code == 'SUMMER':
                if customer_type == 'premium':
                    total += item['price'] * 0.6
                else:
                    total += item['price'] * 0.7
            else:
                if customer_type == 'premium':
                    total += item['price'] * 0.85
                else:
                    total += item['price'] * 0.9
        else:
            if discount_code:
                total += item['price'] * 0.9
            else:
                total += item['price']

    if discount_code == 'VIP20':
        total = total * 0.8

    return total


def process_order(order_data):
    if order_data:
        if 'items' in order_data:
            if len(order_data['items']) > 0:
                if 'customer' in order_data:
                    result = calculate_total(
                        order_data['items'],
                        order_data.get('discount_code'),
                        order_data['customer'].get('type'),
                        order_data.get('is_holiday', False)
                    )
                    return result
                else:
                    return None
            else:
                return 0
        else:
            return None
    else:
        return None
