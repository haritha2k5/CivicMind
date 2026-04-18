// frontend/src/api/civicmindAPI.js

const BASE_URL = "http://localhost:8000";

export async function askPolicyPulse(question) {
  const res = await fetch(`${BASE_URL}/policy-pulse`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function submitGrievance(issue) {
  const res = await fetch(`${BASE_URL}/grievance`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ issue }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function matchSchemes(profile) {
  const res = await fetch(`${BASE_URL}/scheme-match`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
