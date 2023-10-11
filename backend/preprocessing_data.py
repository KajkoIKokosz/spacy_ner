import json
import random

from backend.db import execute_query


def prepare_data_(number_of_rows: int, filename: str):
    query = f"SELECT * FROM rba.address_point ORDER BY uuid_id ORDER BY uuid_id LIMIT {number_of_rows};"
    results = execute_query(query)

    with open(filename, 'w+', encoding="utf-8") as f:
        f.write('[')
        # Print the results
        for row in results:
            voivodeship = row[6] or ""
            county = row[7] or ""
            community = row[8] or ""
            city = row[9] or ""
            street = row[14] or ""
            housenumber = row[16] or ""
            zipcode = row[17] or ""

            addr_point = f'{voivodeship} {county} {community} {city} {street} {housenumber} {zipcode}'
            # entities
            voivodeship_ent = [0, len(voivodeship), "VOIVODESHIP"]
            caret = len(voivodeship) + 1
            county_ent = [caret, caret + len(county), "COUNTY"]
            caret += len(county) + 1
            community_ent = [caret, caret + len(community), "COMMUNITY"]
            caret += len(community) + 1
            city_ent = [caret, caret + len(city), "CITY"]
            caret += len(city) + 1
            street_ent = [caret, caret + len(street), "STREET"]
            caret += len(street) + 1
            housenumber_ent = [caret, caret + len(housenumber), "HOUSENUMBER"]
            caret += len(housenumber) + 1
            zipcode_ent = [caret, caret + len(zipcode), "ZIPCODE"]

            entities = [voivodeship_ent, county_ent, community_ent, city_ent, street_ent, housenumber_ent, zipcode_ent]
            addr_data = [addr_point, {"entities": entities}]
            addr_data = json.dumps(addr_data, ensure_ascii=False)
            f.write(addr_data + ',\n')
        f.write(']')


def prepare_data(number_of_rows: int, filename: str):
    query = f"SELECT * FROM rba.address_point WHERE numerporzadkowy is not null and ulic_nazwa_1 is not null limit {number_of_rows};"
    results = execute_query(query)

    with open(filename, 'w+', encoding="utf-8") as f:
        f.write('[')
        for i, row in enumerate(results):
            voivodeship = row[6] or ""
            city = row[9] or ""
            street = row[14] or ""
            housenumber = row[16] or ""
            zipcode = row[17] or ""

            addr_point = [(voivodeship, 'VOIVODESHIP'), (city, 'CITY'), (street, 'STREET'),
                          (housenumber, 'HOUSENUMBER'), (zipcode, 'ZIPCODE')]
            random.shuffle(addr_point)

            caret = 0
            addr_data = []
            entities = []
            addr_str = ''
            for shuf_addr in addr_point:
                addr_str += f'{shuf_addr[0]} '
                entities.append([caret, caret + len(shuf_addr[0]), shuf_addr[1]])
                addr_data.append(entities)
                caret += len(shuf_addr[0]) + 1
            addr_data = [addr_str, {"entities": entities}]
            addr_data = json.dumps(addr_data, ensure_ascii=False)
            if i < len(results) - 1:
                addr_data += ',\n'
            f.write(addr_data)
        f.write(']')
