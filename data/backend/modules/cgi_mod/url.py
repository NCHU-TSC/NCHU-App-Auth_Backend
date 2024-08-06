import urllib

def build_url(url: str, params: dict[str] = None, filiter: list = [None]): # filiter: list of values to be removed
    if params is None or len(params) == 0:
        return url
    else:
        new_params = {}
        if filiter is not None:
            for key, value in params.items():
                if value not in filiter:
                    new_params[key] = value
        else:
            new_params = params

        return url + '?' + urllib.parse.urlencode(new_params)