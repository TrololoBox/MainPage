import * as React from "react";
export function TooltipProvider({ children }: React.PropsWithChildren) {
  return <>{children}</>;
}
export function Tooltip({ children }: React.PropsWithChildren) {
  return <span className="tooltip">{children}</span>;
}
export function TooltipTrigger({ asChild, children, ...props }: any) {
  return React.cloneElement(children, props);
}
export function TooltipContent({ children }: React.PropsWithChildren) {
  return <span className="tooltip-content">{children}</span>;
}
