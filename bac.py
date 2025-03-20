import requests
from flask import Response

def basic_bac(urls,headers_lower, headers_higher):    
    
    if not urls:
        return None
    
    methods = ["GET", "POST", "DELETE", "PATCH", "PUT"]
    results = {}

    for url in urls:
        for method in methods:
            try:
                response_admin = requests.request(method, url, headers=headers_higher)
                admin_content = response_admin.text
                admin_status = response_admin.status_code

                response_user = requests.request(method, url, headers=headers_lower)
                user_content = response_user.text
                user_status = response_user.status_code

                results[(url, method)] = {
                    "admin_status": admin_status,
                    "user_status": user_status,
                    "admin_content": admin_content,
                    "user_content": user_content,
                    "url": url,
                    "method": method
                }

            except Exception as e:
                print(f"Exception occured in bac.py : {e}")
    return results
