import requests
from analyze_resp import resp_analyze
from process_Form import process_form_n_cookie
from gen_report import save_report_as_html
from payload import generate_header_bypass_report
# List of headers to be sent
headers = {
    "X-Originally-Forwarded-For": "127.0.0.1",
    "X-Originating-": "127.0.0.1, 68.180.194.242",
    "X-Originating-IP": "127.0.0.1, 68.180.194.242",
    "True-Client-IP": "127.0.0.1, 68.180.194.242",
    "X-WAP-Profile": "127.0.0.1, 68.180.194.242",
    "Profile": "{url-in-context}",
    "X-Arbitrary": "{url-in-context}",
    "X-HTTP-DestinationURL": "{url-in-context}",
    "X-Forwarded-Proto": "{url-in-context}",
    "Destination": "127.0.0.1, 68.180.194.242",
    "Proxy": "127.0.0.1, 68.180.194.242",
    "CF-Connecting_IP": "127.0.0.1, 68.180.194.242",
    "Referer": "{url-in-context}",
    "X-Custom-IP-Authorization": "127.0.0.1",
    "X-Remote-IP": "127.0.0.1",
    "X-Client-IP": "127.0.0.1",
    "X-Host": "127.0.0.1",
    "X-Forwarded-Host": "127.0.0.1",
    "X-Original-URL": "{url-in-context}",
    "X-Rewrite-URL": "{url-in-context}",
    "Content-Length": "0",
    "X-ProxyUser-Ip": "127.0.0.1",
    "Base-Url": "127.0.0.1",
    "Client-IP": "127.0.0.1",
    "Http-Url": "127.0.0.1",
    "Proxy-Host": "127.0.0.1",
    "Proxy-Url": "127.0.0.1",
    "Real-Ip": "127.0.0.1",
    "Redirect": "127.0.0.1",
    "Referrer": "127.0.0.1",
    "Request-Uri": "127.0.0.1",
    "Uri": "127.0.0.1",
    "X-Forward-For": "127.0.0.1",
    "X-Forwarded-By": "127.0.0.1",
    "X-Forwarded-For-Original": "127.0.0.1",
    "X-Forwarded-Server": "127.0.0.1",
    "X-Forwarded": "127.0.0.1",
    "X-Forwarder-For": "127.0.0.1",
    "X-Http-Destinationurl": "127.0.0.1",
    "X-Http-Host-Override": "127.0.0.1",
    "X-Original-Remote-Addr": "127.0.0.1",
    "X-Proxy-Url": "127.0.0.1",
    "X-Real-Ip": "127.0.0.1",
    "X-Remote-Addr": "127.0.0.1",
    "X-OReferrer": "https0X0P+00.0000000.000000www.google.com0.000000"
}

# Function to send requests
def send_custom_header_request(form_data,flag):
    result = []
    vuln_header = []
    vuln_content = []
    url,cookie = process_form_n_cookie(form_data)  # Extract URL from the form

    for key, value in headers.items():
        # Replace {url-in-context} with the actual URL value
        header_value = value.replace("{url-in-context}", url) if "{url-in-context}" in value else value

        # Create a single-header dictionary for the current request
        single_header = {key: header_value}

        try:
            cookies = {"session_token": cookie}
            # Sending a GET request with a single header
            response = requests.get(url, headers=single_header,cookies=cookies)
            if response.status_code == 200:
                resp_res = resp_analyze(url, response.content)
            else:
                resp_res = None

            response_entry = {
                "header": key,
                "value": header_value,
                "status": response.status_code
            }

            # Update the dictionary if resp_res indicates vulnerability
            if resp_res == 'Y':
                response_entry["Result after response analysis"] = "VULNERABLE"
                vuln_header.append(header_value)
                vuln_content.append(response.content)
                flag = 1

            # Append the final dictionary to responses
            result.append(response_entry)

        except requests.RequestException as e:
            # Handle errors similarly
            result.append({
                "header": key,
                "value": header_value,
                "status": f"Error: {str(e)}"
            })
    if vuln_header:
        try:
            report = generate_header_bypass_report(url,vuln_header,vuln_content)
            save_report_as_html(report)
        except:
            print("Report generation failed")
    return result,flag

def header_inj_bac(urls,headers_lower,headers_higher):
    results = {}
    for key, value in headers.items():
        # Replace {url-in-context} with the actual URL value
        header_value = value.replace("{url-in-context}", url) if "{url-in-context}" in value else value

        # Create a single-header dictionary for the current request
        single_header = {key: header_value}

        #Combine both headers into single dictionary
        lower_combined_headers = single_header | headers_lower
        higher_combined_headers = single_header | headers_higher
        try:
            for url in urls:
                response_admin = requests.get(url,headers=higher_combined_headers)
                admin_content = response_admin.text
                admin_status = response_admin.status_code

                response_user = requests.get(url,headers=lower_combined_headers)
                user_content = response_user.text
                user_status = response_user.status_code

                results[(url)] = {
                    "admin_status": admin_status,
                    "user_status": user_status,
                    "admin_content": admin_content,
                    "user_content": user_content,
                    "url": url,
                    "header": single_header
                }
        except:
            print("Error occured while sending GET request")
    return results