
import * as React from "react";
export function Switch({ checked, onCheckedChange, ...props }: {checked:boolean; onCheckedChange:(v:boolean)=>void} & React.HTMLAttributes<HTMLButtonElement>){
  return <button className={`switch ${checked?'on':''}`} onClick={()=>onCheckedChange(!checked)} {...props}><span className="switch-dot"/></button>
}
