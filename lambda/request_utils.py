def check_response_code(response):
    if response.status_code != 200:
        print(response.text)
        raise Exception('Request failed')
