import requests
import time

def main():
    # STEP 1 - Call generateWebhook
    url_generate = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
    headers_generate = {
        "Content-Type": "application/json"
    }
    body_generate = {
        "name": "Lavesh Sewani",
        "regNo": "0827AL231065",
        "email": "laveshsewani231284@acropolis.in"
    }

    try:
        response = requests.post(url_generate, headers=headers_generate, json=body_generate)
        data = response.json()
        
        webhook = data.get("webhook")
        access_token = data.get("accessToken")
        
        print(f"Webhook: {webhook}")
        print(f"AccessToken: {access_token}")
        
    except Exception as e:
        print(f"Error in Step 1: {e}")
        return

    # STEP 2 - SQL Query
    sql_query = "SELECT e1.EMP_ID, e1.FIRST_NAME, e1.LAST_NAME, d.DEPARTMENT_NAME, COUNT(e2.EMP_ID) AS YOUNGER_EMPLOYEES_COUNT FROM EMPLOYEE e1 JOIN DEPARTMENT d ON e1.DEPARTMENT = d.DEPARTMENT_ID LEFT JOIN EMPLOYEE e2 ON e1.DEPARTMENT = e2.DEPARTMENT AND e2.DOB > e1.DOB GROUP BY e1.EMP_ID, e1.FIRST_NAME, e1.LAST_NAME, d.DEPARTMENT_NAME ORDER BY e1.EMP_ID DESC"

    # STEP 3 - Submit to webhook
    if not webhook or not access_token:
        print("Missing webhook or access token. Exiting.")
        return

    headers_submit = {
        "Authorization": access_token,
        "Content-Type": "application/json"
    }
    body_submit = {
        "finalQuery": sql_query
    }

    max_retries = 4
    delay = 2

    for attempt in range(max_retries + 1):
        try:
            res = requests.post(webhook, headers=headers_submit, json=body_submit)
            print(f"Response Status: {res.status_code}")
            print(f"Response Body: {res.text}")
            
            if res.status_code == 200:
                break
            else:
                if attempt < max_retries:
                    time.sleep(delay)
        except Exception as e:
            print(f"Error in Step 3: {e}")
            if attempt < max_retries:
                time.sleep(delay)

if __name__ == "__main__":
    main()