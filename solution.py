import requests
import time

def main():
    # STEP 1
    url_generate = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
    payload = {
        "name": "Lavesh Sewani",
        "regNo": "0827AL231065",
        "email": "laveshsewani231284@acropolis.in"
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        print(f"Calling {url_generate}...")
        response1 = requests.post(url_generate, json=payload, headers=headers)
        response1.raise_for_status()
        data1 = response1.json()
        
        webhook = data1.get("webhook")
        access_token = data1.get("accessToken")
        
        print(f"Webhook: {webhook}")
        print(f"AccessToken: {access_token}")
        
        if not webhook or not access_token:
            print("Failed to extract webhook or accessToken from response.")
            return

        # STEP 2
        sql_query = """SELECT e1.EMP_ID, e1.FIRST_NAME, e1.LAST_NAME, 
d.DEPARTMENT_NAME, COUNT(e2.EMP_ID) AS 
YOUNGER_EMPLOYEES_COUNT FROM EMPLOYEE e1 
JOIN DEPARTMENT d ON e1.DEPARTMENT = d.DEPARTMENT_ID 
LEFT JOIN EMPLOYEE e2 ON e1.DEPARTMENT = e2.DEPARTMENT 
AND e2.DOB > e1.DOB GROUP BY e1.EMP_ID, e1.FIRST_NAME, 
e1.LAST_NAME, d.DEPARTMENT_NAME 
ORDER BY e1.EMP_ID DESC"""

        # STEP 3
        headers2 = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }
        payload2 = {
            "finalQuery": sql_query
        }
        
        max_retries = 4
        retry_delay = 2
        
        print(f"\nCalling {webhook}...")
        for attempt in range(max_retries + 1):
            response2 = requests.post(webhook, json=payload2, headers=headers2)
            
            print(f"Attempt {attempt + 1}: Status Code {response2.status_code}")
            print(f"Response: {response2.text}")
            
            if response2.status_code == 200:
                print("Successfully submitted the query.")
                break
            else:
                if attempt < max_retries:
                    print(f"Request failed. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print("All retries exhausted.")
                    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
