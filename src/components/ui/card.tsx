import * as React from "react";
export function Card(
  props: React.PropsWithChildren<{ className?: string; style?: React.CSSProperties }>,
) {
  return (
    <div className={`card ${props.className || ""}`} style={props.style}>
      {props.children}
    </div>
  );
}
export function CardHeader(props: React.PropsWithChildren<{ className?: string }>) {
  return <div className={`card-header ${props.className || ""}`}>{props.children}</div>;
}
export function CardContent(props: React.PropsWithChildren<{ className?: string }>) {
  return <div className={`card-body ${props.className || ""}`}>{props.children}</div>;
}
export function CardTitle(props: React.PropsWithChildren<{ className?: string }>) {
  return <h3 className={props.className || ""}>{props.children}</h3>;
}
export function CardDescription(
  props: React.PropsWithChildren<{ className?: string; style?: React.CSSProperties }>,
) {
  return (
    <p className={props.className || ""} style={props.style}>
      {props.children}
    </p>
  );
}
