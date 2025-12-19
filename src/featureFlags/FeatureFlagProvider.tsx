import { PropsWithChildren, createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from "react";

import { fetchFeatureFlags } from "./api";
import { defaultFeatureFlags } from "./config";
import { FeatureFlagContextValue, FeatureFlags } from "./types";

const FeatureFlagContext = createContext<FeatureFlagContextValue | undefined>(undefined);

export function FeatureFlagProvider({ children }: PropsWithChildren) {
  const [flags, setFlags] = useState<FeatureFlags>(defaultFeatureFlags);
  const [isLoading, setIsLoading] = useState(false);
  const [lastUpdated, setLastUpdated] = useState<Date>();
  const [error, setError] = useState<string | null>(null);
  const abortRef = useRef<AbortController>();

  const loadFeatureFlags = useCallback(async (signal?: AbortSignal) => {
    setIsLoading(true);
    setError(null);
    try {
      const remoteFlags = await fetchFeatureFlags(signal);
      setFlags((current) => ({ ...current, ...remoteFlags }));
      setLastUpdated(new Date());
    } catch (err) {
      if (signal?.aborted) return;
      console.warn("Feature flags fallback to defaults", err);
      setError("Не удалось загрузить фичефлаги. Используем значения по умолчанию.");
    } finally {
      if (!signal?.aborted) setIsLoading(false);
    }
  }, []);

  const startLoadingFlags = useCallback(() => {
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    loadFeatureFlags(controller.signal);
  }, [loadFeatureFlags]);

  useEffect(() => {
    startLoadingFlags();

    return () => {
      abortRef.current?.abort();
    };
  }, [startLoadingFlags]);

  const isEnabled = useCallback((key: string) => Boolean(flags[key]), [flags]);

  const value = useMemo<FeatureFlagContextValue>(
    () => ({
      flags,
      isLoading,
      lastUpdated,
      isEnabled,
      error,
      reload: startLoadingFlags,
    }),
    [flags, isLoading, isEnabled, lastUpdated, error, startLoadingFlags],
  );

  return <FeatureFlagContext.Provider value={value}>{children}</FeatureFlagContext.Provider>;
}

export function useFeatureFlags(): FeatureFlagContextValue {
  const ctx = useContext(FeatureFlagContext);
  if (!ctx) {
    throw new Error("useFeatureFlags must be used within FeatureFlagProvider");
  }
  return ctx;
}

export function useFeatureFlag(key: string): boolean {
  const { isEnabled } = useFeatureFlags();
  return isEnabled(key);
}
