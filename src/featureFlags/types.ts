export type FeatureFlags = Record<string, boolean>;

export interface FeatureFlagContextValue {
  flags: FeatureFlags;
  isLoading: boolean;
  lastUpdated?: Date;
  isEnabled: (key: string) => boolean;
}
