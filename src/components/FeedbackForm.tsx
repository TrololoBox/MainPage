import { FormEvent, useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

type FormState = "idle" | "submitting" | "success" | "error";

export function FeedbackForm() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [status, setStatus] = useState<FormState>("idle");
  const [error, setError] = useState("");

  const errorMessageId = "feedback-error";
  const statusMessageId = "feedback-status";

  const isSubmitDisabled = useMemo(
    () =>
      status === "submitting" ||
      name.trim().length < 2 ||
      !email.includes("@") ||
      message.trim().length < 10,
    [email, message, name, status],
  );

  const resetError = () => {
    if (error) setError("");
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setStatus("submitting");
    setError("");

    try {
      const response = await fetch(`${API_BASE_URL}/feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, message }),
      });

      if (!response.ok) {
        try {
          const body = await response.json();
          const fieldError = body?.detail?.[0]?.msg ?? "Не удалось отправить заявку. Попробуйте ещё раз.";
          setError(fieldError);
        } catch {
          setError("Сервис временно недоступен. Попробуйте позже или напишите в поддержку.");
        }
        setStatus("error");
        return;
      }

      setStatus("success");
    } catch (err) {
      console.error("Feedback submit failed", err);
      setError("Сбой сети. Проверьте подключение и повторите отправку.");
      setStatus("error");
    }
  };

  return (
    <Card className="feedback-card">
      <CardHeader>
        <CardTitle>Рассказать про задачу</CardTitle>
        <CardDescription>Оставьте контакты — пришлём подборку инструментов и короткое демо.</CardDescription>
      </CardHeader>
      <CardContent>
        <form className="feedback-form" onSubmit={handleSubmit} aria-busy={status === "submitting"}>
          <div className="grid gap-3">
            <div className="form-field">
              <Label htmlFor="name">Имя</Label>
              <Input
                id="name"
                name="name"
                value={name}
                onChange={(e) => {
                  setName(e.target.value);
                  resetError();
                }}
                placeholder="Мария"
                required
                aria-invalid={Boolean(error)}
                aria-describedby={error ? errorMessageId : undefined}
              />
            </div>
            <div className="form-field">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                name="email"
                type="email"
                value={email}
                onChange={(e) => {
                  setEmail(e.target.value);
                  resetError();
                }}
                placeholder="you@example.com"
                required
                aria-invalid={Boolean(error)}
                aria-describedby={error ? errorMessageId : undefined}
              />
            </div>
            <div className="form-field">
              <Label htmlFor="message">Опишите задачу</Label>
              <textarea
                id="message"
                name="message"
                className="input textarea"
                value={message}
                minLength={10}
                onChange={(e) => {
                  setMessage(e.target.value);
                  resetError();
                }}
                placeholder="Например: нужно быстро подготовить PDF из таблицы с графиками"
                required
                aria-invalid={Boolean(error)}
                aria-describedby={error ? errorMessageId : undefined}
              />
              <p className="hint">Минимум 10 символов. Можно оставить ссылку на пример.</p>
            </div>
          </div>
          {error && (
            <p className="error-text" role="alert" id={errorMessageId} aria-live="assertive">
              {error}
            </p>
          )}
          {status === "success" ? (
            <p className="success-text" role="status" aria-live="polite" id={statusMessageId}>
              Спасибо! Мы ответим на email в течение рабочего дня.
            </p>
          ) : (
            <div className="feedback-actions">
              <Button disabled={isSubmitDisabled} type="submit" variant="default">
                {status === "submitting" ? "Отправляем…" : "Отправить заявку"}
              </Button>
              <p className="muted">7 дней бесплатно + подборка инструментов под ваш кейс.</p>
            </div>
          )}
        </form>
      </CardContent>
    </Card>
  );
}
