def setStatusResponse(response: dict, status: dict):
    response['status'] = 'success' if status['code'][-2:] == '.0' else 'fail'
    response['reason'] = status
    return response