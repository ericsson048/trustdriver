const trimTrailingSlash = (value: string) => value.replace(/\/+$/, '');

const isAbsoluteUrl = (value: string) => /^https?:\/\//i.test(value);

const normalizeBasePath = (value: string) => {
  const trimmed = trimTrailingSlash(value.trim());
  if (!trimmed) {
    return '/api';
  }

  if (isAbsoluteUrl(trimmed)) {
    return trimmed;
  }

  return trimmed.startsWith('/') ? trimmed : `/${trimmed}`;
};

const getAppOrigin = () => {
  if (typeof window !== 'undefined' && window.location.origin) {
    return window.location.origin;
  }

  return '';
};

const rawApiBase = import.meta.env.VITE_API_BASE_URL ?? '/api';
const rawAppBaseUrl = import.meta.env.VITE_APP_BASE_URL ?? getAppOrigin();

export const apiConfig = {
  apiBaseUrl: normalizeBasePath(rawApiBase),
  appBaseUrl: trimTrailingSlash(rawAppBaseUrl),
};

export const apiUrl = (path: string) =>
  `${apiConfig.apiBaseUrl}${path.startsWith('/') ? path : `/${path}`}`;

export const apiFetch: typeof fetch = (input, init) =>
  fetch(input, {
    credentials: 'include',
    ...init,
  });

export const appUrl = (path: string) => {
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  return apiConfig.appBaseUrl ? `${apiConfig.appBaseUrl}${normalizedPath}` : normalizedPath;
};

export const sharedFileUrl = (token: string) => appUrl(`/shared/${token}`);
