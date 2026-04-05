import React, { useMemo, useState } from "react";
import type { DoctorVisitListItem } from "../../types/doctor";
import { DoctorVisitCard } from "./DoctorVisitCard";
import { EmptyState } from "../shared/EmptyState";

const tabs: Array<{ label: string; value: string }> = [
  { label: "All", value: "all" },
  { label: "Active", value: "active" },
  { label: "Scheduled", value: "scheduled" },
  { label: "Completed", value: "completed" },
];

export function DoctorVisitList({ visits, onOpen }: { visits: DoctorVisitListItem[]; onOpen: (visitId: string) => void }) {
  const [activeTab, setActiveTab] = useState("all");
  const filtered = useMemo(
    () => visits.filter((visit) => activeTab === "all" || visit.status === activeTab),
    [visits, activeTab]
  );

  return (
    <div>
      <div className="tab-row">
        {tabs.map((tab) => (
          <button
            key={tab.value}
            className={tab.value === activeTab ? "tab-button tab-button--active" : "tab-button"}
            onClick={() => setActiveTab(tab.value)}
          >
            {tab.label}
          </button>
        ))}
      </div>
      {filtered.length === 0 ? (
        <EmptyState title="No visits in this view" description="Once visits are created, they will appear here for workspace access." />
      ) : (
        <div className="visit-grid">
          {filtered.map((visit) => (
            <DoctorVisitCard key={visit.id} visit={visit} onOpen={onOpen} />
          ))}
        </div>
      )}
    </div>
  );
}
