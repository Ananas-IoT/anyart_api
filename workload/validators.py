# LOCATION
# 3. check if it's registered
# 4. get district
# 5. if it's in monument db
# --build restrictions


import json
from pprint import pprint
import requests

url = 'https://opendata.city-adm.lviv.ua/api/3/action/datastore_search'


class APIError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "APIError: status={}".format(self.status)


def is_in_monument_db(adress_building, adress_street):
    parameters = {"resource_id": "d8dfe789-167d-4074-be39-d661c666e08d",
                  "fields": {
                      # '_id','adress_street', 'adress_building', 'adress_notes',
                      'architect_decision_doctype'}, \
                  "filters": '{"adress_building": "' + str(adress_building) + '",'
                                                                              '"adress_street": "' + str(
                      adress_street) + '" }',
                  "limit": 5,  # set amount of result records
                  'records_format': 'lists'  # can be objects, lists, csv and tsv
                  }
    headers = {'Content-Type': 'application/json'}

    response = requests.get(url, params=parameters, headers=headers)
    print(response.status_code)

    if response.status_code != 200:

        raise APIError(response.status_code)
    else:
        data = json.loads(response.text)
        # json_data = json.JSONEncoder(indent=None,
        #                              separators=(',', ': ')).encode(data)
        # pprint(json_data)
        # print(type(data))
        restriction_list = []
        monuments_list = data['result']['records']
        architect_decision_doctype = 4

        for i in range(0, len(monuments_list)):
            #print(monuments_list[i])
            monuments_list[i][0] = monuments_list[i][0].replace('"', " ")
            #print(monuments_list[i][0])
            restriction_list.append({#"authority": 0,
                                     # "reason": json.loads(json.dumps(monuments_list[i][0])),
                                     "reason": monuments_list[i][0],
                                     # "reason":"Ann",
                                     })

        # print(json.dumps(result, indent=4))
        # print(response.content)
    return restriction_list


if __name__ == '__main__':
    print(is_in_monument_db("2.0", "Азовська"))
