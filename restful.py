#!/usr/bin/env python3

import argparse
import json
import csv
import requests

class RestfulClient:
    BASE_URL = 'https://jsonplaceholder.typicode.com'

    def __init__(self, method, endpoint, data=None, output=None):
        self.method = method
        self.endpoint = endpoint
        self.data = data
        self.output = output

    def make_request(self):
        url = f'{self.BASE_URL}{self.endpoint}'
        headers = {'Content-Type': 'application/json'}

        if self.method == 'get':
            response = requests.get(url)
        elif self.method == 'post':
            response = requests.post(url, data=self.data, headers=headers)
        else:
            raise ValueError(f'Invalid method: {self.method}')

        return response

    def handle_response(self, response):
        print(f'Status Code: {response.status_code}')

        if response.status_code // 100 != 2:
            print(f'Error: {response.text}')
            exit(1)

        if self.output:
            self.save_response(response.text)

        print(response.text)

    def save_response(self, response_text):
        if self.output.endswith('.json'):
            with open(self.output, 'w') as json_file:
                json.dump(json.loads(response_text), json_file, indent=2)
               
        elif self.output.endswith('.csv'):
            data = json.loads(response_text)
            keys = data[0].keys() if isinstance(data, list) and data else []
            with open(self.output, 'w', newline='') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=keys)
                csv_writer.writeheader()
                csv_writer.writerows(data)
        else:
            print(f'Unsupported output format: {self.output}')
            exit(1)

def main():
    parser = argparse.ArgumentParser(description='Command-line REST client for JSONPlaceholder.')
    parser.add_argument('method', choices=['get', 'post'], help='Request method')
    parser.add_argument('endpoint', help='Request endpoint URI fragment')
    parser.add_argument('-d', '--data', help='Data to send with request')
    parser.add_argument('-o', '--output', help='Output to .json or .csv file (default: dump to stdout)')

    args = parser.parse_args()

    restful_client = RestfulClient(args.method, args.endpoint, args.data, args.output)
    response = restful_client.make_request()
    restful_client.handle_response(response)

if __name__ == '__main__':
    main()
