import * as React from "react";
export function Skeleton({ className = "" }: { className?: string }) {
  return <div className={className} style={{ background: "#eee", borderRadius: 6, height: 12 }} />;
}
