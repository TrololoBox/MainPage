import * as React from "react";
const Ctx = React.createContext<{
  open: string | null;
  setOpen: (v: string | null) => void;
  collapsible?: boolean;
} | null>(null);
export function Accordion({
  type,
  collapsible,
  className = "",
  children,
}: {
  type: "single";
  collapsible?: boolean;
  className?: string;
  children: React.ReactNode;
}) {
  const [open, setOpen] = React.useState<string | null>(null);
  return (
    <div className={className}>
      <Ctx.Provider value={{ open, setOpen, collapsible }}>{children}</Ctx.Provider>
    </div>
  );
}
export function AccordionItem({
  value,
  className = "",
  children,
}: {
  value: string;
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <div className={className} data-value={value}>
      {children}
    </div>
  );
}
export function AccordionTrigger({
  children,
  className = "",
  ...rest
}: React.ButtonHTMLAttributes<HTMLButtonElement> & { className?: string }) {
  const ctx = React.useContext(Ctx)!;
  const value = (rest as any)["data-parent"] as string | undefined;
  const v = value || "";
  const isOpen = ctx.open === v;
  return (
    <button
      className={className}
      onClick={() => ctx.setOpen(isOpen && ctx.collapsible ? null : v)}
      {...rest}
    >
      {children}
    </button>
  );
}
export function AccordionContent({
  children,
  className = "",
}: React.PropsWithChildren<{ className?: string }>) {
  return (
    <div className={className} style={{ paddingBottom: 12 }}>
      {children}
    </div>
  );
}
