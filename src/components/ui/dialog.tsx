
import * as React from "react";
type Props = { open:boolean; onOpenChange:(v:boolean)=>void; children: React.ReactNode; };
const Ctx = React.createContext<{open:boolean; setOpen:(v:boolean)=>void} | null>(null);
export function Dialog({ open, onOpenChange, children }: Props){
  return <Ctx.Provider value={{ open, setOpen:onOpenChange }}>{children}</Ctx.Provider>;
}
export function DialogContent({ className='', style, children }: React.PropsWithChildren<{className?:string; style?:React.CSSProperties}>){
  const ctx = React.useContext(Ctx)!;
  if(!ctx.open) return null;
  return (<>
    <div className="dialog-overlay" onClick={()=>ctx.setOpen(false)} />
    <div className={`dialog ${className}`} style={style}>{children}</div>
  </>);
}
export function DialogHeader({ children }: React.PropsWithChildren){ return <div className="card-header">{children}</div>; }
export function DialogFooter({ children }: React.PropsWithChildren){ return <div className="card-body" style={{display:'flex',justifyContent:'flex-end',gap:8}}>{children}</div>; }
export function DialogTitle({ children }: React.PropsWithChildren){ return <h3>{children}</h3>; }
export function DialogDescription({ children }: React.PropsWithChildren){ return <p style={{color:'var(--secondary)'}}>{children}</p>; }
