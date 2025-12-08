import * as React from "react";
export function Badge({
  children,
  className = "",
  style,
}: React.PropsWithChildren<{ className?: string; style?: React.CSSProperties }>) {
  return (
    <span className={`badge ${className}`} style={style}>
      {children}
    </span>
  );
}
