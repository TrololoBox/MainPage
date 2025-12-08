import * as React from "react";
export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "outline" | "ghost";
  className?: string;
}
export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = "primary", className = "", ...props }, ref) => {
    const cls = [
      "btn",
      variant === "primary" ? "btn-primary" : variant === "outline" ? "btn-outline" : "btn-ghost",
      className,
    ].join(" ");
    return <button ref={ref} className={cls} {...props} />;
  },
);
Button.displayName = "Button";
export default Button;
