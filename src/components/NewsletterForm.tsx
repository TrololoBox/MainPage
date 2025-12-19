import { FormEvent, useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

type FormState = "idle" | "submitting" | "success" | "error";

export function NewsletterForm() {
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [status, setStatus] = useState<FormState>("idle");
  const [error, setError] = useState("");

  const errorMessageId = "newsletter-error";
  const statusMessageId = "newsletter-status";

  const isSubmitDisabled = useMemo(
    () => status === "submitting" || !email.includes("@") || (name && name.trim().length < 2),
    [email, name, status],
  );

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setStatus("submitting");
    setError("");

    try {
      const response = await fetch(`${API_BASE_URL}/newsletter`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, name: name || undefined }),
      });

      if (!response.ok) {
        try {
          const body = await response.json();
          const fieldError = body?.detail ?? "Не удалось подписаться. Попробуйте ещё раз.";
          setError(fieldError);
        } catch {
          setError("Сервис временно недоступен. Попробуйте отправить форму позже.");
        }
        setStatus("error");
        return;
      }

      setStatus("success");
    } catch (err) {
      console.error("Newsletter subscribe failed", err);
      setError("Сбой сети. Проверьте подключение и повторите попытку.");
      setStatus("error");
    }
  };

  return (
    <Card className="feedback-card">
      <CardHeader>
        <CardTitle>Подписаться на обновления</CardTitle>
        <CardDescription>
          Получайте новости о свежих инструментах и релизах ProstoKit. Никакого спама.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form className="feedback-form" onSubmit={handleSubmit} aria-busy={status === "submitting"}>
          <div className="grid gap-3">
            <div className="form-field">
              <Label htmlFor="newsletter-email">Email</Label>
              <Input
                id="newsletter-email"
                name="email"
                type="email"
                value={email}
                onChange={(e) => {
                  setEmail(e.target.value);
                  setError("");
                }}
                placeholder="you@example.com"
                required
                aria-invalid={Boolean(error)}
                aria-describedby={error ? errorMessageId : undefined}
              />
            </div>
            <div className="form-field">
              <Label htmlFor="newsletter-name">Имя (необязательно)</Label>
              <Input
                id="newsletter-name"
                name="name"
                value={name}
                onChange={(e) => {
                  setName(e.target.value);
                  setError("");
                }}
                placeholder="Как к вам обращаться"
                aria-invalid={Boolean(error)}
                aria-describedby={error ? errorMessageId : undefined}
              />
            </div>
          </div>
          {error && (
            <p className="error-text" role="alert" id={errorMessageId} aria-live="assertive">
              {error}
            </p>
          )}
          {status === "success" ? (
            <p
              className="success-text"
              role="status"
              aria-live="polite"
              id={statusMessageId}
            >
              Готово! Проверьте почту — первое письмо уже в пути.
            </p>
          ) : (
            <div className="feedback-actions">
              <Button disabled={isSubmitDisabled} type="submit" variant="default">
                {status === "submitting" ? "Подписываем…" : "Подписаться"}
              </Button>
              <p className="muted">Пара писем в месяц, отписаться можно в один клик.</p>
            </div>
          )}
        </form>
      </CardContent>
    </Card>
  );
}
