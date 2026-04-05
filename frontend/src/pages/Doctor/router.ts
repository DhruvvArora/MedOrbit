export type AppRoute =
  | { name: "doctor-dashboard" }
  | { name: "doctor-workspace"; visitId: string }
  | { name: "doctor-review"; visitId: string }
  | { name: "doctor-live-consultation" }
  | { name: "doctor-live-consultation-review" };

export function parseRoute(pathname: string): AppRoute {
  if (pathname === "/doctor/dashboard" || pathname === "/") return { name: "doctor-dashboard" };
  
  if (pathname === "/doctor/live-consultation") return { name: "doctor-live-consultation" };
  if (pathname === "/doctor/live-consultation/review") return { name: "doctor-live-consultation-review" };

  const workspaceMatch = pathname.match(/^\/doctor\/visits\/([^/]+)\/workspace$/);
  if (workspaceMatch) return { name: "doctor-workspace", visitId: workspaceMatch[1] };

  const reviewMatch = pathname.match(/^\/doctor\/visits\/([^/]+)\/review$/);
  if (reviewMatch) return { name: "doctor-review", visitId: reviewMatch[1] };

  return { name: "doctor-dashboard" };
}

export function navigate(path: string) {
  window.history.pushState({}, "", path);
  window.dispatchEvent(new PopStateEvent("popstate"));
}
