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
  const { data, loading, error, refresh } = useAsyncResource(() => doctorApi.getDashboard(), []);

  if (loading) return <LoadingState label="Loading doctor dashboard..." />;
  if (error || !data) return <ErrorState message={error || "Dashboard unavailable"} onRetry={() => void refresh()} />;

  return (
    <DoctorShell
      title={`Welcome, ${data.doctor_name}`}
      subtitle="Transcript-first, doctor-in-the-loop consultation workflow"
      actions={<button onClick={() => void refresh()}>Refresh</button>}
    >
      <DoctorDashboardStats counts={data.counts} />
      <DoctorVisitList visits={data.visits} onOpen={(visitId) => navigate(`/doctor/visits/${visitId}/workspace`)} />
    </DoctorShell>
  );
}
