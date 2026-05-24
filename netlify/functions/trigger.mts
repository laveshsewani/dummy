import type { Context, Config } from "@netlify/functions";

export default async (req: Request, context: Context) => {
  // Only allow POST requests
  if (req.method !== "POST") {
    return new Response(
      JSON.stringify({ error: "Method Not Allowed. Use POST." }),
      {
        status: 405,
        headers: { "Content-Type": "application/json" }
      }
    );
  }

  try {
    // 1. Generate Webhook
    const urlGenerate = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON";
    const payload1 = {
      name: "Lavesh Sewani",
      regNo: "0827AL231065",
      email: "laveshsewani231284@acropolis.in"
    };

    const response1 = await fetch(urlGenerate, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload1)
    });

    if (!response1.ok) {
      const errorText = await response1.text();
      return new Response(
        JSON.stringify({ error: `Failed to generate webhook: ${errorText}` }),
        { status: response1.status, headers: { "Content-Type": "application/json" } }
      );
    }

    const data1: any = await response1.json();
    const webhook = data1.webhook;
    const accessToken = data1.accessToken;

    if (!webhook || !accessToken) {
      return new Response(
        JSON.stringify({ error: "Invalid generateWebhook response: missing webhook or accessToken" }),
        { status: 500, headers: { "Content-Type": "application/json" } }
      );
    }

    // 2. SQL Query definition
    const sqlQuery = `SELECT e1.EMP_ID, e1.FIRST_NAME, e1.LAST_NAME, 
d.DEPARTMENT_NAME, COUNT(e2.EMP_ID) AS 
YOUNGER_EMPLOYEES_COUNT FROM EMPLOYEE e1 
JOIN DEPARTMENT d ON e1.DEPARTMENT = d.DEPARTMENT_ID 
LEFT JOIN EMPLOYEE e2 ON e1.DEPARTMENT = e2.DEPARTMENT 
AND e2.DOB > e1.DOB GROUP BY e1.EMP_ID, e1.FIRST_NAME, 
e1.LAST_NAME, d.DEPARTMENT_NAME 
ORDER BY e1.EMP_ID DESC`;

    // 3. Submit Webhook
    const response2 = await fetch(webhook, {
      method: "POST",
      headers: {
        "Authorization": accessToken,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ finalQuery: sqlQuery })
    });

    const response2Text = await response2.text();
    let response2Body;
    try {
      response2Body = JSON.parse(response2Text);
    } catch {
      response2Body = response2Text;
    }

    return new Response(
      JSON.stringify({
        success: response2.ok,
        step1: {
          webhook: webhook,
          accessToken: accessToken
        },
        step3: {
          status: response2.status,
          body: response2Body
        }
      }),
      {
        status: 200,
        headers: { "Content-Type": "application/json" }
      }
    );

  } catch (err: any) {
    return new Response(
      JSON.stringify({ error: err.message || "An unexpected error occurred." }),
      {
        status: 500,
        headers: { "Content-Type": "application/json" }
      }
    );
  }
};

export const config: Config = {
  path: "/api/trigger"
};
