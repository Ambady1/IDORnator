import random
from urllib.parse import urlparse

import requests

def generate_endpoint_variations(endpoint):
    variations = set()
    
    # Basic variations
    variations.add(endpoint.upper())
    variations.add(endpoint.lower())

    # Capitalize first letter of each part (split by hyphen or slash)
    parts = [part.capitalize() for part in endpoint.split('/')]
    variations.add('/'.join(parts))

    # Replace hyphens with underscores
    variations.add(endpoint.replace('-', '_'))

    # Random character case toggles (just a few random samples)
    for _ in range(3):  # number of random variations
        random_variation = ''.join(
            c.upper() if random.choice([True, False]) else c.lower()
            for c in endpoint
        )
        variations.add(random_variation)

    return list(variations)

def capital_bypass(urls, headers_lower, headers_higher):
    if not urls:
        return None
    try:
        results = {}
        for url in urls:
            parsed_url = urlparse(url)
            endpoint = parsed_url.path
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            variations = generate_endpoint_variations(endpoint)

            for variation in variations:
                new_url = f"{base_url}{variation}"

                print(f"[!] Testing: {new_url}")
                try:
                    response_user = requests.get(new_url, headers=headers_lower, timeout=5)
                    user_content = response_user.text
                    user_status = response_user.status_code

                    response_admin = requests.get(new_url, headers=headers_higher,timeout=5)
                    admin_content = response_admin.text
                    admin_status = response_admin.status_code

                    results[(url)] = {
                    "admin_status": admin_status,
                    "user_status": user_status,
                    "admin_content": admin_content,
                    "user_content": user_content,
                    "url": url,
                    "variation": new_url
                }
                except requests.exceptions.RequestException as e:
                    print(f"[!] Error requesting {new_url}: {e}\n")

        return results            
    except Exception as e:
        print(e)
    return
