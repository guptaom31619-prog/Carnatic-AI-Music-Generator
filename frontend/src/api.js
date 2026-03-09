const BASE_URL = "http://localhost:8000";

async function handleResponse(res) {
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail ?? "Request failed");
  }
  return res;
}

export async function getRagas() {
  const res = await fetch(`${BASE_URL}/ragas`);
  await handleResponse(res);
  return res.json();
}

export async function getInstruments() {
  const res = await fetch(`${BASE_URL}/instruments`);
  await handleResponse(res);
  return res.json();
}

export async function getPresets() {
  const res = await fetch(`${BASE_URL}/presets`);
  await handleResponse(res);
  return res.json();
}

export async function getPresetDetail(presetId) {
  const res = await fetch(`${BASE_URL}/presets/${presetId}`);
  await handleResponse(res);
  return res.json();
}

export async function generateMusic(data) {
  const res = await fetch(`${BASE_URL}/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  await handleResponse(res);
  return res.json();
}

export function getDownloadUrl(midiPath) {
  const filename = midiPath.split("/").pop();
  return `${BASE_URL}/download/${filename}`;
}
