import json

from http import client
from xml.etree import ElementTree

from uszipcode import SearchEngine


def request_document(domain: str, relative_url: str) -> str:
    connection = client.HTTPSConnection(domain)
    connection.request("GET", relative_url)
    response = connection.getresponse()
    document = response.read()
    connection.close()
    return document


def parse_xml_to_dict(xml_document: str) -> list:
    xml_tree = ElementTree.fromstring(xml_document)

    def parse(xml):
        parsed_dict = {}
        for childNode in xml:
            if len(childNode):
                parsed_dict[childNode.tag] = parse(childNode)
            else:
                parsed_dict[childNode.tag] = childNode.text
        return parsed_dict

    return [parse(childNode) for childNode in xml_tree]


def parse_address(address_string: str) -> list:
    """
    This parses the address using the library uszipcode.
    This library considers 'Washington' a city and 'DC' the state.
    """
    address = {}

    address['postal'] = int(address_string[-5:])
    address_string = address_string.replace(f' {address["postal"]}', '')

    search = SearchEngine(simple_zipcode=True)
    search_results = search.by_zipcode(address['postal']).to_dict()

    address['state'] = search_results['state']
    address['city'] = search_results['major_city']

    address_string = address_string.replace(f' {address["city"]} {address["state"]}', '')
    address['street'] = address_string.strip()

    return [address]


def format_senator_data(data: dict) -> dict:
    formatted_data = []
    data.pop() # Removes the 'Last Updated' element
    for d in data:
        senator = {}
        senator['firstName'] = d['first_name']
        senator['lastName'] = d['last_name']
        senator['fullName'] = f'{senator["firstName"]} {senator["lastName"]}'
        senator['chartId'] = d['bioguide_id']
        senator['mobile'] = d['phone']
        senator['address'] = parse_address(d['address'].strip())
        formatted_data.append(senator)
    return formatted_data


if __name__ == '__main__':
    domain = 'www.senate.gov'
    relative_url = '/general/contact_information/senators_cfm.xml'
    xml_senators = request_document(domain, relative_url)
    unformatted_senators = parse_xml_to_dict(xml_senators)
    formatted_senators = format_senator_data(unformatted_senators)
    json_senators = json.dumps(formatted_senators)
    # Uncomment to write to file in the same directory (easier to read IMO)
    # with open('senators.json', 'w') as out_file:
    #     json.dump(formatted_senators, out_file)
    print(json_senators)
