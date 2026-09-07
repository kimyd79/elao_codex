export const featureFlags = {
  reactV2Enabled: import.meta.env.VITE_REACT_V2_ENABLED !== 'false',
  vueFallbackUrl: import.meta.env.VITE_VUE_FALLBACK_URL ?? '/mwla/',
} as const
