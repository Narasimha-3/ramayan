def get_result(prompt):
    import requests
    URL = "http://127.0.0.1:8000/post"
    PARAMS = {'post':"who is rama"}
    r = requests.post(url = URL, params = PARAMS)
    return r.json().get('response'), r.json().get('source_nodes')