import { PropsWithChildren, createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";

import { fetchFeatureFlags } from "./api";
import { defaultFeatureFlags } from "./config";
import { FeatureFlagContextValue, FeatureFlags } from "./types";

const FeatureFlagContext = createContext<FeatureFlagContextValue | undefined>(undefined);

export function FeatureFlagProvider({ children }: PropsWithChildren) {
  const [flags, setFlags] = useState<FeatureFlags>(defaultFeatureFlags);
  const [isLoading, setIsLoading] = useState(false);
  const [lastUpdated, setLastUpdated] = useState<Date>();

  useEffect(() => {
    let isMounted = true;

    async function loadFeatureFlags() {
      setIsLoading(true);
      try {
        const remoteFlags = await fetchFeatureFlags();
        if (!isMounted) return;
        setFlags((current) => ({ ...current, ...remoteFlags }));
        setLastUpdated(new Date());
      } catch (error) {
        console.warn("Feature flags fallback to defaults", error);
      } finally {
        if (isMounted) setIsLoading(false);
      }
    }

    loadFeatureFlags();

    return () => {
      isMounted = false;
    };
  }, []);

  const isEnabled = useCallback((key: string) => Boolean(flags[key]), [flags]);

  const value = useMemo<FeatureFlagContextValue>(
    () => ({
      flags,
      isLoading,
      lastUpdated,
      isEnabled,
    }),
    [flags, isLoading, isEnabled, lastUpdated],
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
