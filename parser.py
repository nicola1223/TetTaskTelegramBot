import requests
from excel_parser import get_sku


def get_feedbacks():
    """
    Function to get feedbacks for products in Excel
    :return: tuple of ratings, rating and product name
    """
    s = requests.Session()

    for sku in get_sku():
        sku = str(sku)
        response = s.get(f'https://basket-04.wbbasket.ru/vol{sku[:3]}/part{sku[:5]}/{sku}/info/ru/card.json')

        imt_id = response.json()['imt_id']
        imt_name = response.json()['imt_name']

        response = s.get(f'https://feedbacks1.wb.ru/feedbacks/v1/{imt_id}')
        yield response.json()["feedbacks"], response.json()["valuation"], imt_name, sku


def get_bad_responses():
    for feedbacks, rating, name, sku in get_feedbacks():
        for feedback in feedbacks:
            if feedback["productValuation"] < 4:
                yield name, sku, feedback["productValuation"], feedback["text"], rating
