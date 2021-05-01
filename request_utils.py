def check_response_code(response):
    if response.status_code != 200:
        print(response)
        raise Exception('Request failed')
