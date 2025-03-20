import time
import requests  # Ensure this is installed
from flask import Flask, render_template, request, stream_with_context, Response, session
from bac import basic_bac
from capitalization import capital_bypass
from idor import send_idor
from custom_header import header_inj_bac, send_custom_header_request
from path_Traversal import path_trav
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secure key


@app.route("/", methods=["GET", "POST"])
def home():
    """Render the home page and handle form submission."""
    if request.method == "POST":
        mode = request.form.get("mode")

        if mode == "IDOR":
            session["idor_form_data"] = request.form.to_dict()
            return render_template("idor.html", form_data=session["idor_form_data"])
        
        elif mode == "BAC":
            session["bac_form_data"] = request.form.to_dict()
            return render_template("bac.html")

    return render_template("home.html")


@app.route("/idor-stream", methods=["GET"])
def idor_stream():
    """Stream IDOR testing results incrementally using Server-Sent Events (SSE)."""
    form_data = session.get("idor_form_data")

    if not form_data:
        return Response("data: Error: No form data found.\n\n", content_type="text/event-stream")

    @stream_with_context
    def generate_results():
        flag = 0
        yield "data: Creating intelligent payloads using AI...\n\n"

        # Step 1: Test IDOR
        try:
            result1, flag = send_idor(form_data, flag)
            for entry in result1:
                analysis_result = entry.get("Result after response analysis", "")
                text_color = "text-green" if analysis_result == "VULNERABLE" else "text-red"

                yield f"data: <div class='result-item {text_color}'>" \
                      f"<p><strong>URL:</strong> {entry['url']}</p>" \
                      f"<p><strong>Payload:</strong> {entry['payload']}</p>" \
                      f"<p><strong>Status:</strong> {entry['status']}</p>" \
                      f"{f'<p><strong>Analysis:</strong> {analysis_result}</p>' if analysis_result else ''}" \
                      f"</div><hr>\n\n" 
        except Exception as e:
            yield f"data: Error in IDOR testing: {str(e)}\n\n"
            return

        # Step 2: Test Custom Headers
        if flag == 0:
            yield "data: Moving to second phase of testing...\n\n"
            time.sleep(5)
            try:
                result2, flag = send_custom_header_request(form_data, flag)
                for entry in result2:
                    analysis_result = entry.get("Result after response analysis", "")
                    text_color = "text-green" if analysis_result == "VULNERABLE" else "text-red"

                    yield f"data: <div class='result-item {text_color}'>" \
                          f"<p><strong>Header:</strong> {entry['header']}</p>" \
                          f"<p><strong>Value:</strong> {entry['value']}</p>" \
                          f"<p><strong>Status:</strong> {entry['status']}</p>" \
                          f"{f'<p><strong>Analysis:</strong> {analysis_result}</p>' if analysis_result else ''}" \
                          f"</div><hr>\n\n"
            except Exception as e:
                yield f"data: Error in custom header testing: {str(e)}\n\n"
                return

        # Step 3: Test Path Traversal
        if flag == 0:
            yield "data: Moving to third phase of testing...\n\n"
            time.sleep(5)
            try:
                result3, flag = path_trav(form_data, flag)
                for entry in result3:
                    analysis_result = entry.get("Result after response analysis", "")
                    text_color = "text-green" if analysis_result == "VULNERABLE" else "text-red"

                    yield f"data: <div class='result-item {text_color}'>" \
                          f"<p><strong>URL:</strong> {entry['url']}</p>" \
                          f"<p><strong>Status:</strong> {entry['status']}</p>" \
                          f"{f'<p><strong>Analysis:</strong> {analysis_result}</p>' if analysis_result else ''}" \
                          f"</div><hr>\n\n"
            except Exception as e:
                yield f"data: Error in path traversal testing: {str(e)}\n\n"
                return

        yield "data: Testing completed.\n\n"

    return Response(generate_results(), content_type="text/event-stream")


@app.route("/bac-stream", methods=["GET"])
def bac_stream():
    """Stream the results of BAC testing."""
    bac_form_data = session.get("bac_form_data")

    if not bac_form_data:
        return Response("data: Error: No form data found.\n\n", content_type="text/event-stream")
    try:
        with open("BacURLs.txt", "r") as file:
            urls = [line.strip() for line in file.readlines() if line.strip()]
    except Exception as e:
        return Response(f"Exception Occured while reading BacUrls.txt : {e}")
    #print("BAC Form Data Retrieved:", bac_form_data) 
   
    @stream_with_context
    def generate_results():
        bac_flag = 0
        yield "data: Starting BAC Testing...\n\n"

        lower_token = bac_form_data.get("lower_token")
        higher_token = bac_form_data.get("higher_token")

        yield f"data: Lower privilage token : {lower_token}\n\n"
        yield f"data: Higher privilage token : {higher_token}\n\n"

        # Validate required fields
        if not lower_token or not higher_token:
            yield "data: Error: Missing required parameters.\n\n"
            return

        #print("Form Data Received:", bac_form_data)
        headers_lower = {"Authorization": f"Bearer {lower_token}"}
        headers_higher = {"Authorization": f"Bearer {higher_token}"}

        #1.Basic BAC testing
        try:
            yield f"data: Checking access control mechanisms...\n\n"
            time.sleep(5)
            results = basic_bac(urls,headers_lower,headers_higher)
            #print(results)
            for key,result in results.items():
                if (result["user_status"] == result["admin_status"] and result["user_content"] == result["admin_content"]):
                    bac_flag=1
                    yield f"data: <div class='result-item text-green'>"
                    yield f"<p><strong>Vulnerable:</strong> Lower privilage token can perform {result["method"]} actions on {result["url"]} </p></div><hr>\n\n"    
                else:
                    yield f"data: <div class='result-item text-red'>"
                    yield f"<p><strong>Secure:</strong> Access control works for {result["method"]} on {result["url"]}.</p></div><hr>\n\n"
        except Exception as e:
            yield "data: Error Testing BAC!!!\n\n"
            return

        #2.Header Injection Bypass
        if bac_flag == 0:
            yield f"data: Moving To Second Phase Of Testing - Header Injection\n\n"
            time.sleep(5)
            try:
                results = header_inj_bac(urls,headers_lower,headers_higher)
                for url,result in results.items():
                    if (result["user_status"] == result["admin_status"] and result["user_content"] == result["admin_content"]):
                        bac_flag=1
                        yield f"data: <div class='result-item text-green'>"
                        yield f"<p><strong>Vulnerable:</strong> Lower privilage token can perform GET actions on {result["url"]} </p></div><hr>\n\n"
                    else:
                        yield f"data: <div class='result-item text-red'>"
                        yield f"<p><strong>Secure:</strong> Access control works for GET on {result["url"]}.</p></div><hr>\n\n"       
            except Exception as e:
                yield f"data: Error Occured While Testing Header Injection For BAC\n\n"

        #3.Endpoint Capitalization
        if bac_flag == 0:
            yield f"data: Moving To Third Phase Of Testing - Endpoint Capitalization\n\n"
            time.sleep(5)
            try:
                results = capital_bypass(urls,headers_lower,headers_higher)
                for url,result in results.items():
                    if (result["user_status"] == result["admin_status"] and result["user_content"] == result["admin_content"]):
                        bac_flag=1
                        yield f"data: <div class='result-item text-green'>"
                        yield f"<p><strong>Vulnerable:</strong> Lower Privilage Token Can Perform GET Actions Using Payload {result["variation"]} </p></div><hr>\n\n"
                    else:
                        yield f"data: <div class='result-item text-red'>"
                        yield f"<p><strong>Secure:</strong> Access control works for GET on {result["url"]}. Access attempt using {result["variation"]} failed</p></div><hr>\n\n"
            except:
                yield f"data: Error Occured While Testing Endpoint Capitalization For BAC : {str(e)}\n\n"          
        yield "data: BAC Testing Completed.\n\n" 

    return Response(generate_results(), content_type="text/event-stream") 



if __name__ == "__main__":
    app.run(debug=True)
