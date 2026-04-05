import React from "react";
import { useAsyncResource } from "../../hooks/useAsyncResource";
import { doctorApi } from "../../lib/api/doctor";
import { DoctorShell } from "../../components/doctor/DoctorShell";
import { DoctorDashboardStats } from "../../components/doctor/DoctorDashboardStats";
import { DoctorVisitList } from "../../components/doctor/DoctorVisitList";
import { LoadingState } from "../../components/shared/LoadingState";
import { ErrorState } from "../../components/shared/ErrorState";
import { navigate } from "./router";

export function DoctorDashboardPage() {
  const { data, loading, refreshing, error, refresh } = useAsyncResource(() => doctorApi.getDashboard(), []);

  if (loading) return <LoadingState label="Loading doctor dashboard..." />;
  if (error || !data) return <ErrorState message={error || "Dashboard unavailable"} onRetry={() => void refresh("initial")} />;

  return (
    <DoctorShell
      title={`Welcome, ${data.doctor_name}`}
      subtitle="Review visits, track consult progress, and finalize patient-ready plans."
      actions={
        <button onClick={() => void refresh("soft")} disabled={refreshing}>
          {refreshing ? "Refreshing..." : "Refresh"}
        </button>
      }
    >
      <DoctorDashboardStats counts={data.counts} />
      <DoctorVisitList visits={data.visits} onOpen={(visitId) => navigate(`/doctor/visits/${visitId}/workspace`)} />
    </DoctorShell>
  );
}