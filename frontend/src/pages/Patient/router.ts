/**
 * Patient-side route parser.
 * Mirrors the doctor-side router pattern exactly.
 */

export type PatientRoute =
  | { name: "patient-dashboard" }
  | { name: "patient-visit-detail"; visitId: string };

export function parsePatientRoute(pathname: string): PatientRoute {
  if (pathname === "/patient/dashboard" || pathname === "/patient") {
    return { name: "patient-dashboard" };
  }

  const visitMatch = pathname.match(/^\/patient\/visits\/([^/]+)$/);
  if (visitMatch) {
    return { name: "patient-visit-detail", visitId: visitMatch[1] };
  }

  // Fallback → dashboard
  return { name: "patient-dashboard" };
}

export function navigate(path: string) {
  window.history.pushState({}, "", path);
  window.dispatchEvent(new PopStateEvent("popstate"));
}
