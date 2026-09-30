"use client";

import * as React from "react";
import { CoverflowCarousel, CoverflowSlide } from "@/components/ui/coverflow-carousel";

const HISTORICAL_INDIAN_DAMS: CoverflowSlide[] = [
  {
    src: "https://upload.wikimedia.org/wikipedia/commons/1/1a/Machchhu_River_watershed.jpg",
    alt: "Machchhu River Basin and Morbi Dam Failure",
    title: "Machchhu-II Dam (1979)",
    subtitle: "Morbi, Gujarat · Overtopping Failure",
    meta: [
      { label: "Year", value: "1979" },
      { label: "Location", value: "Morbi, Gujarat" },
      { label: "Fatalities", value: "1,800 to 25,000 reported" },
      { label: "Trigger", value: "Catchment Cloudburst" },
    ],
  },
  {
    src: "https://upload.wikimedia.org/wikipedia/commons/c/cd/Panshet_Dam.JPG",
    alt: "Panshet Dam (Tanajisagar) Pune Maharashtra",
    title: "Panshet Dam (1961)",
    subtitle: "Pune, Maharashtra · Conduit Piping Failure",
    meta: [
      { label: "Year", value: "1961" },
      { label: "Location", value: "Pune, Maharashtra" },
      { label: "Fatalities", value: "~1,000 reported" },
      { label: "Trigger", value: "Conduit Seepage & Piping" },
    ],
  },
  {
    src: "https://upload.wikimedia.org/wikipedia/commons/2/29/Tighra_Dam_Gwalior.JPG",
    alt: "Tigra Dam near Gwalior Madhya Pradesh",
    title: "Tigra Dam (1917)",
    subtitle: "Gwalior, Madhya Pradesh · Foundation Sliding",
    meta: [
      { label: "Year", value: "1917" },
      { label: "Location", value: "Gwalior, Madhya Pradesh" },
      { label: "Fatalities", value: "~1,000 reported" },
      { label: "Trigger", value: "Sandstone Bedding Sliding" },
    ],
  },
  {
    src: "https://images.unsplash.com/photo-1578328819058-b69f3a3b0f6b?w=800&auto=format&fit=crop&q=80",
    alt: "Kaddam Dam Spillway and Reservoir Telangana",
    title: "Kaddam Dam (1958 & 1995)",
    subtitle: "Nirmal, Telangana · Spillway Overtopping",
    meta: [
      { label: "Year", value: "1958 & 1995" },
      { label: "Location", value: "Nirmal, Telangana" },
      { label: "Fatalities", value: "Casualties minimized by warning" },
      { label: "Trigger", value: "Inflow exceeding design 2x" },
    ],
  },
  {
    src: "https://upload.wikimedia.org/wikipedia/commons/1/1c/River_Teesta.jpg",
    alt: "Teesta River Gorge and Chungthang Dam Sikkim",
    title: "Chungthang / Teesta-III (2023)",
    subtitle: "Chungthang, Sikkim · GLOF Breach Surge",
    meta: [
      { label: "Year", value: "2023" },
      { label: "Location", value: "Chungthang, Sikkim" },
      { label: "Fatalities", value: "~100 reported / missing" },
      { label: "Trigger", value: "South Lhonak GLOF Wave" },
    ],
  },
];

export default function HistoricalDamsCarouselDemo() {
  const [activeIncident, setActiveIncident] = React.useState(0);

  return (
    <div className="w-full bg-background py-8 px-4">
      <div className="text-center max-w-2xl mx-auto mb-6">
        <h2 className="text-2xl font-bold tracking-tight text-foreground">
          Historical Dam-Break Events in India
        </h2>
        <p className="text-sm text-muted-foreground mt-2">
          Click or swipe any card to examine documented historical failure mechanics and downstream impacts.
        </p>
      </div>

      <CoverflowCarousel
        slides={HISTORICAL_INDIAN_DAMS}
        showCaption={true}
        showPagination={true}
        showNavigation={true}
        onSelect={(idx) => setActiveIncident(idx)}
      />
    </div>
  );
}
