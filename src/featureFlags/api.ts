import { FeatureFlags } from "./types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function fetchFeatureFlags(): Promise<FeatureFlags> {
  const response = await fetch(`${API_BASE_URL}/feature-flags`);

  if (!response.ok) {
    throw new Error(`Failed to load feature flags: ${response.status}`);
  }

  const payload: Array<{ name: string; enabled: boolean }> = await response.json();
  return payload.reduce<FeatureFlags>((acc, flag) => {
    acc[flag.name] = flag.enabled;
    return acc;
  }, {});
}
