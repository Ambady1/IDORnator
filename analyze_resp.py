import requests
from payload import analyze_idor

def resp_analyze(payload,resp):
    gen_res = analyze_idor(payload,resp)
    return gen_res
    #print(resp.content)
