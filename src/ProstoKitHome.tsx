import { useEffect, useMemo, useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Switch } from "@/components/ui/switch";
import { Skeleton } from "@/components/ui/skeleton";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { FeedbackForm } from "./components/FeedbackForm";
import { NewsletterForm } from "./components/NewsletterForm";
import { useFeatureFlag, useFeatureFlags } from "./featureFlags/FeatureFlagProvider";
import {
  Menu,
  Search,
  Shield,
  Sparkles,
  Lock,
  ChevronRight,
  Check,
  ArrowRight,
  LogIn,
  CreditCard,
  Star,
  Image as ImageIcon,
  FileText,
  FileSpreadsheet,
  FileAudio2,
  ScanText,
  Type as TypeIcon,
  Sun,
  Moon,
  ExternalLink,
} from "lucide-react";

const TOKENS = {
  light: {
    accent: "#8A2432",
    text: "#111111",
    secondary: "#666666",
    border: "#E5E7EB",
    bg: "#F8F9FB",
  },
  dark: {
    accent: "#9D2A3A",
    text: "#EDEDED",
    secondary: "#A1A1AA",
    border: "#1F2430",
    bg: "#0B0B0E",
  },
};

const content = {
  brand: "ProstoKit",
  tagline: "Мелкие задачи — в один клик.",
  sub: "Обрезать фото, сделать графики из Excel, потренить печать — быстро и без рекламы.",
  ctaPrimary: "Попробовать бесплатно",
  ctaSecondary: "Посмотреть инструменты",
  micro: { free7: "7 дней бесплатно", noreg: "Без регистрации до 3 операций", privacy: "Приватно" },
  pricing: { title: "Тарифы", pro: 99, trial: 7, currency: "₽/мес" },
  faq: [
    {
      q: "Нужно ли регистрироваться?",
      a: "Нет. До 3 операций доступно без регистрации. Для истории и пресетов — создайте аккаунт.",
    },
    {
      q: "Какие ограничения в бесплатной версии?",
      a: "Лимит по размеру файла 10 МБ, до 3 операций в день, без batch-режима.",
    },
    {
      q: "Что входит в Pro?",
      a: "Повышенные лимиты, пакетная обработка, история, пресеты, приоритетная очередь.",
    },
    {
      q: "Как вы храните файлы?",
      a: "Локально в браузере, где возможно. Серверные операции — с авто-удалением в течение 24 часов.",
    },
    {
      q: "Могу ли я отменить подписку в любой момент?",
      a: "Да, отмена в один клик в настройках — доступ сохраняется до конца оплаченного периода.",
    },
  ],
  how: {
    title: "Как это работает",
    steps: [
      {
        title: "Выберите инструмент",
        desc: "Каталог задач по форматам и действиям.",
        icon: <Sparkles size={24} aria-hidden />,
      },
      {
        title: "Загрузите файл",
        desc: "Укажите параметры, всё понятно и просто.",
        icon: <ImageIcon size={24} aria-hidden />,
      },
      {
        title: "Получите результат",
        desc: "Моментально, без рекламы и воды.",
        icon: <Check size={24} aria-hidden />,
      },
    ],
    why: "80% операций — прямо в браузере. Остальное — безопасно на сервере с авто-удалением.",
  },
  benefits: [
    {
      title: "Скорость",
      desc: "80% в браузере — без загрузок.",
      icon: <Sparkles size={20} aria-hidden />,
    },
    {
      title: "Приватность",
      desc: "Временное хранение, авто-удаление.",
      icon: <Lock size={20} aria-hidden />,
    },
    {
      title: "Без рекламы",
      desc: "Чистый интерфейс — без баннеров.",
      icon: <Shield size={20} aria-hidden />,
    },
    {
      title: "История и пресеты",
      desc: "Сохраняйте параметры и повторяйте.",
      icon: <Star size={20} aria-hidden />,
    },
  ],
};

const TOOLS: Array<{
  id: string;
  name: string;
  category: "Type" | "Image" | "Excel" | "PDF" | "Audio" | "OCR";
  bullets: string[];
  pro: boolean;
  icon: JSX.Element;
  tags: string[];
}> = [
  {
    id: "type",
    name: "Type",
    category: "Type",
    bullets: ["Тренажёр печати", "Скорость/ошибки"],
    pro: false,
    icon: <TypeIcon size={28} aria-hidden />,
    tags: ["текст", "навыки", "клавиатура"],
  },
  {
    id: "image",
    name: "Image",
    category: "Image",
    bullets: ["Обрезка, сжатие", "Водяной знак"],
    pro: false,
    icon: <ImageIcon size={28} aria-hidden />,
    tags: ["png", "jpg", "resize"],
  },
  {
    id: "excel",
    name: "Excel",
    category: "Excel",
    bullets: ["Графики из таблиц", "CSV ⇄ XLSX"],
    pro: true,
    icon: <FileSpreadsheet size={28} aria-hidden />,
    tags: ["таблицы", "chart", "csv"],
  },
  {
    id: "pdf",
    name: "PDF",
    category: "PDF",
    bullets: ["Объединить/разделить", "Сжать PDF"],
    pro: true,
    icon: <FileText size={28} aria-hidden />,
    tags: ["merge", "split", "compress"],
  },
  {
    id: "audio",
    name: "Audio",
    category: "Audio",
    bullets: ["Обрезать/склеить", "Кодеки/битрейт"],
    pro: true,
    icon: <FileAudio2 size={28} aria-hidden />,
    tags: ["mp3", "wav", "trim"],
  },
  {
    id: "ocr",
    name: "OCR",
    category: "OCR",
    bullets: ["Текст с изображений", "PDF → TXT"],
    pro: true,
    icon: <ScanText size={28} aria-hidden />,
    tags: ["распознавание", "text", "scan"],
  },
];

const computeYearlyDiscount = (price: number) => Math.round(price * 0.75 * 100) / 100; // −25%

function track(event: string, payload?: Record<string, unknown>) {
  const entry = { event, ts: new Date().toISOString(), ...payload };
  // @ts-ignore
  window.dataLayer = window.dataLayer || [];
  // @ts-ignore
  window.dataLayer.push(entry);
  console.log("[analytics]", entry);
}

function Pill({ children, dark }: { children: React.ReactNode; dark: boolean }) {
  return (
    <span
      className="pill"
      style={{ background: dark ? "rgba(157,42,58,0.12)" : "rgba(138,36,50,0.1)" }}
    >
      {children}
    </span>
  );
}

function Toast({ message, onClose }: { message: string; onClose: () => void }) {
  useEffect(() => {
    const t = setTimeout(onClose, 2400);
    return () => clearTimeout(t);
  }, [onClose]);
  return (
    <div
      role="status"
      style={{
        position: "fixed",
        top: 16,
        right: 16,
        background: "#111",
        color: "#fff",
        padding: "10px 14px",
        borderRadius: 14,
        zIndex: 50,
      }}
    >
      {message}
    </div>
  );
}

function DevTests({ priceMonth }: { priceMonth: number }) {
  const [results, setResults] = useState<{ name: string; pass: boolean; details?: string }[]>([]);
  const [running, setRunning] = useState(false);
  const run = () => {
    setRunning(true);
    const out: { name: string; pass: boolean; details?: string }[] = [];
    const push = (name: string, pass: boolean, details?: string) =>
      out.push({ name, pass, details });
    try {
      // @ts-ignore
      const okIcon = typeof ExternalLink === "function" || typeof ExternalLink === "object";
      push("ExternalLink импортирован", !!okIcon, okIcon ? "ok" : "нет");
      push("TOOLS.length === 6", TOOLS.length === 6, `len=${TOOLS.length}`);
      const q = "pdf";
      const found = TOOLS.filter((t) =>
        (t.name + " " + t.tags.join(" ") + " " + t.bullets.join(" ")).toLowerCase().includes(q),
      );
      push(
        "Поиск 'pdf' находит элементы",
        found.length > 0,
        `found=${found.map((f) => f.id).join(",")}`,
      );
      const expected = 74.25;
      const calc = computeYearlyDiscount(99);
      push("Годовая цена 99→74.25", Math.abs(calc - expected) < 0.0001, `calc=${calc}`);
      // @ts-ignore
      const before = (window.dataLayer || []).length;
      track("test_event_dev"); // @ts-ignore
      const after = (window.dataLayer || []).length;
      push("track() пушит в dataLayer", after > before, `before=${before}, after=${after}`);
      push(
        "CTA тексты заданы",
        !!content.ctaPrimary && !!content.ctaSecondary,
        `${content.ctaPrimary} / ${content.ctaSecondary}`,
      );
    } catch (e: any) {
      push("Исключение при прогоне тестов", false, String(e?.message || e));
    }
    setResults(out);
    setRunning(false);
  };
  useEffect(run, []);
  const passed = results.filter((r) => r.pass).length;
  return (
    <Card className="card">
      <CardHeader>
        <CardTitle className="">Тесты (для QA)</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="">
          Прогон автотестов: {passed}/{results.length} пройдено.
        </div>
        <ul>
          {results.map((r, i) => (
            <li
              key={`${r.name}-${i}`}
              style={{ display: "flex", alignItems: "center", gap: 8, margin: "6px 0" }}
            >
              <span
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  justifyContent: "center",
                  width: 20,
                  height: 20,
                  borderRadius: 999,
                  background: r.pass ? "#10B981" : "#F43F5E",
                  color: "#fff",
                }}
              >
                {r.pass ? "✓" : "!"}
              </span>
              <span>{r.name}</span>
              {r.details && <span style={{ marginLeft: 8, opacity: 0.7 }}>({r.details})</span>}
            </li>
          ))}
        </ul>
        <div style={{ paddingTop: 8 }}>
          <Button onClick={run} disabled={running} variant="outline">
            {running ? "Запуск…" : "Перезапустить тесты"}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}

export default function ProstoKitHome() {
  const [dark, setDark] = useState(false);
  useEffect(() => {
    const saved = localStorage.getItem("prostoTheme");
    if (saved) setDark(saved === "dark");
  }, []);
  useEffect(() => {
    localStorage.setItem("prostoTheme", dark ? "dark" : "light");
  }, [dark]);
  useEffect(() => {
    try {
      /* @ts-ignore */ const ok =
        typeof ExternalLink === "function" || typeof ExternalLink === "object";
      console.log("[self-test] ExternalLink import:", ok ? "OK" : "MISSING");
    } catch {}
  }, []);

  const [q, setQ] = useState("");
  const [filter, setFilter] = useState<string>("all");
  const [loading, setLoading] = useState(true);
  const [toastMsg, setToastMsg] = useState<string | null>(null);
  const [mobileMenu, setMobileMenu] = useState(false);
  const [signinOpen, setSigninOpen] = useState(false);
  const [paywallOpen, setPaywallOpen] = useState(false);
  const [yearly, setYearly] = useState(false);
  const {
    isLoading: featureFlagsLoading,
    lastUpdated: featureFlagsUpdatedAt,
    error: featureFlagsError,
    reload: reloadFeatureFlags,
  } = useFeatureFlags();
  const newsletterEnabled = useFeatureFlag("newsletter_form");
  const feedbackEnabled = useFeatureFlag("feedback_form");
  const betaBannerEnabled = useFeatureFlag("beta_tools_banner");
  useEffect(() => {
    const t = setTimeout(() => setLoading(false), 600);
    return () => clearTimeout(t);
  }, []);

  const catalogRef = useRef<HTMLDivElement | null>(null);
  useEffect(() => {
    const el = catalogRef.current;
    if (!el) return;
    let fired = false;
    const io = new IntersectionObserver(
      (entries) =>
        entries.forEach((e) => {
          if (e.isIntersecting && e.intersectionRatio >= 0.6 && !fired) {
            fired = true;
            track("scroll_catalog_view", { ratio: e.intersectionRatio });
          }
        }),
      { threshold: [0.6] },
    );
    io.observe(el);
    return () => io.disconnect();
  }, []);

  const filtered = useMemo(() => {
    return TOOLS.filter(
      (t) =>
        (filter === "all" || t.category.toLowerCase() === filter) &&
        (q.trim() === "" ||
          (t.name + " " + t.tags.join(" ") + " " + t.bullets.join(" "))
            .toLowerCase()
            .includes(q.toLowerCase())),
    );
  }, [q, filter]);

  const openTool = (toolId: string, pro: boolean) => {
    track("catalog_card_open", { toolId, pro });
    if (pro) setPaywallOpen(true);
    else setToastMsg("Открыто демо инструмента: " + toolId);
  };
  const onHeroPrimary = () => {
    track("hero_cta_click", { variant: "primary" });
    setSigninOpen(true);
  };
  const onHeroSecondary = () => {
    track("hero_cta_click", { variant: "secondary" });
    (document.querySelector("#catalog") as HTMLElement | null)?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  };

  const priceMonth = content.pricing.pro;
  const priceMonthYearly = computeYearlyDiscount(priceMonth);

  const bg = dark ? TOKENS.dark.bg : TOKENS.light.bg;
  const text = dark ? TOKENS.dark.text : TOKENS.light.text;
  const secondary = dark ? TOKENS.dark.secondary : TOKENS.light.secondary;
  const border = dark ? TOKENS.dark.border : TOKENS.light.border;
  const accent = dark ? TOKENS.dark.accent : TOKENS.light.accent;

  return (
    <TooltipProvider>
      <div style={{ background: bg, color: text, minHeight: "100dvh" }}>
        <header className="header">
          <div className="container header-inner flex items-center justify-between">
            <a href="#top" className="flex items-center gap-3" aria-label="ProstoKit — на главную">
              <div
                style={{
                  width: 32,
                  height: 32,
                  borderRadius: 12,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  background: accent,
                  boxShadow: "var(--shadow-btn)",
                }}
              >
                <Sparkles size={16} color="#fff" />
              </div>
              <span style={{ fontSize: 18, fontWeight: 600 }}>{content.brand}</span>
            </a>
            <nav className="flex items-center gap-6" style={{ fontSize: 14 }}>
              <a href="#catalog">Инструменты</a>
              <a href="#pricing">Цены</a>
              <a href="#how">Как это работает</a>
              <a href="#contact">Консультация</a>
              <a href="#faq">FAQ</a>
            </nav>
            <div className="flex items-center gap-6">
              <Button variant="ghost" onClick={() => setSigninOpen(true)} aria-label="Войти">
                <LogIn size={16} style={{ marginRight: 8 }} />
                Войти
              </Button>
              <Button onClick={onHeroPrimary} aria-label="Попробовать бесплатно">
                {" "}
                {content.ctaPrimary} <ArrowRight size={16} style={{ marginLeft: 8 }} />
              </Button>
              <span className="tooltip">
                <Button
                  variant="ghost"
                  aria-label="Переключить тему"
                  onClick={() => setDark((v) => !v)}
                >
                  {dark ? <Sun size={16} /> : <Moon size={16} />}
                </Button>
                <span className="tooltip-content">Тема: {dark ? "тёмная" : "светлая"}</span>
              </span>
            </div>
          </div>
        </header>

        <section id="top" className="section" style={{ borderTop: "none" }}>
          <div className="container">
            <div className="grid grid-12" style={{ gap: 24, alignItems: "center" }}>
              <div style={{ gridColumn: "span 6" }}>
                <h1 style={{ fontWeight: 600, lineHeight: 1.2 }}>{content.tagline}</h1>
                <p style={{ marginTop: 16, fontSize: 16, color: secondary }}>{content.sub}</p>
                <div className="flex gap-3 wrap" style={{ marginTop: 24 }}>
                  <Button onClick={onHeroPrimary}>
                    {content.ctaPrimary} <ArrowRight size={16} style={{ marginLeft: 8 }} />
                  </Button>
                  <Button variant="outline" onClick={onHeroSecondary}>
                    {content.ctaSecondary}
                  </Button>
                </div>
                <div className="flex gap-3 wrap" style={{ marginTop: 16, fontSize: 14 }}>
                  <span className="pill">🎁 {content.micro.free7}</span>
                  <span className="pill">🪪 {content.micro.noreg}</span>
                  <span className="pill">🔒 {content.micro.privacy}</span>
                </div>
              </div>
              <div style={{ gridColumn: "span 6" }}>
                <Card>
                  <CardHeader>
                    <CardTitle className="">
                      <span style={{ fontSize: 16 }}>Быстрый мокап интерфейса</span>
                    </CardTitle>
                    <CardDescription style={{ color: secondary }}>Лёгкий визуал для LCP ≤ 2.5s</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-3">
                      {["Image", "Excel", "PDF", "Audio", "OCR", "Type"].map((it) => (
                        <div
                          key={it}
                          style={{
                            padding: 12,
                            borderRadius: 12,
                            border: `1px solid ${border}`,
                            fontSize: 14,
                          }}
                        >
                          <div
                            style={{ height: 12, width: 40, borderRadius: 4, background: border }}
                          />
                          <div
                            style={{
                              height: 64,
                              borderRadius: 8,
                              background: dark ? "#151822" : "#F3F4F6",
                              marginTop: 12,
                            }}
                          />
                          <div
                            style={{
                              height: 8,
                              width: "75%",
                              borderRadius: 4,
                              background: border,
                              marginTop: 12,
                            }}
                          />
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        </section>

        {betaBannerEnabled && (
          <section className="section">
            <div className="container">
              <Card className="card" style={{ padding: 24 }}>
                <div className="flex items-center justify-between gap-4 flex-wrap">
                  <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                    <Badge variant="secondary">Beta</Badge>
                    <div>
                      <h3 style={{ fontSize: 18, fontWeight: 600 }}>Новый сценарий: пакетное сжатие файлов</h3>
                      <p style={{ color: secondary, marginTop: 4, fontSize: 14 }}>
                        Фича доступна ограниченно и включена через фичефлаг. Оставьте обратную связь — соберём метрики и
                        включим по умолчанию.
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div role="status" aria-live="polite">
                      {featureFlagsLoading ? (
                        <Skeleton className="h-6 w-48" aria-hidden />
                      ) : featureFlagsError ? (
                        <p style={{ color: secondary, fontSize: 12 }}>
                          {featureFlagsError}
                        </p>
                      ) : (
                        <p style={{ color: secondary, fontSize: 12 }}>
                          Флаги обновлены: {featureFlagsUpdatedAt?.toLocaleString() ?? "только что"}
                        </p>
                      )}
                    </div>
                    {featureFlagsError && (
                      <Button
                        variant="ghost"
                        onClick={reloadFeatureFlags}
                        aria-label="Повторить попытку загрузки фичефлагов"
                      >
                        Обновить
                      </Button>
                    )}
                    <Button variant="outline" onClick={() => track("beta_flag_cta", { feature: "batch_compress" })}>
                      Записаться в бета
                    </Button>
                  </div>
                </div>
              </Card>
            </div>
          </section>
        )}

        <section id="catalog" className="section" ref={catalogRef}>
          <div className="container">
            <div className="flex items-end justify-between wrap gap-6">
              <div>
                <h2 className="">Каталог инструментов</h2>
                <p style={{ color: secondary, marginTop: 4, fontSize: 14 }}>
                  Выберите задачу или найдите по ключевым словам.
                </p>
              </div>
              <div
                className="flex items-center gap-6 wrap"
                style={{ width: "100%", maxWidth: 680 }}
              >
                <div style={{ position: "relative", flex: 1 }}>
                  <Search
                    size={16}
                    style={{
                      position: "absolute",
                      left: 12,
                      top: "50%",
                      transform: "translateY(-50%)",
                      color: secondary,
                    }}
                  />
                  <Input
                    aria-label="Поиск по каталогу"
                    value={q}
                    onChange={(e) => setQ(e.target.value)}
                    placeholder="Поиск: pdf, resize, csv…"
                    className=""
                    style={{ paddingLeft: 34 }}
                  />
                </div>
                <select
                  aria-label="Фильтр по категории"
                  className="input"
                  value={filter}
                  onChange={(e) => setFilter(e.target.value)}
                  style={{ maxWidth: 200 }}
                >
                  <option value="all">Все</option>
                  <option value="image">Image</option>
                  <option value="excel">Excel</option>
                  <option value="pdf">PDF</option>
                  <option value="audio">Audio</option>
                  <option value="ocr">OCR</option>
                  <option value="type">Type</option>
                </select>
              </div>
            </div>

            <div className="grid" style={{ gridTemplateColumns:'repeat(auto-fill, minmax(280px, 1fr))', gap:24, marginTop:24 }}>
              {loading ? Array.from({length:6}).map((_,i)=>(
                <Card key={i}><CardContent>
                  <div className="flex items-center gap-6">
                    <div style={{width:40,height:40,borderRadius:12,background:'#eee'}} />
                    <div style={{flex:1}}>
                      <div style={{height:14, width:'66%', background:'#eee', borderRadius:6}}/>
                      <div style={{height:12, width:'50%', background:'#eee', borderRadius:6, marginTop:8}}/>
                    </div>
                  </div>
                  <div style={{height:12, background:'#eee', borderRadius:6, marginTop:16}}/>
                  <div style={{height:12, width:'70%', background:'#eee', borderRadius:6, marginTop:8}}/>
                  <div className="flex items-center justify-between" style={{marginTop:16}}>
                    <div style={{height:24,width:80,background:'#eee',borderRadius:999}} />
                    <div style={{height:36,width:120,background:'#eee',borderRadius:12}} />
                  </div>
                </CardContent></Card>
              )) : filtered.map((tool)=>(
                <Card key={tool.id}>
                  <CardHeader>
                    <div className="flex items-center" style={{gap:12}}>
                      <div style={{width:40,height:40,borderRadius:12,display:'flex',alignItems:'center',justifyContent:'center', background: '#F3F4F6' }}>{tool.icon}</div>
                      <div style={{flex:1}}>
                        <CardTitle className="">
                          <span style={{ fontSize: 18 }}>{tool.name}</span>
                        </CardTitle>
                        <CardDescription style={{ fontSize:12, color: secondary }}>{tool.category}</CardDescription>
                      </div>
                      {tool.pro && <Badge style={{ background: accent, color:'#fff' }}>В подписке</Badge>}
                    </div>
                  </CardHeader>
                  <CardContent>
                    <ul style={{fontSize:14, color: secondary, display:'grid', gap:6}}>
                      {tool.bullets.map((b) => (
                        <li key={`${tool.id}-${b}`} style={{display:'flex',gap:8,alignItems:'flex-start'}}>
                          <Check size={16} color={accent}/>{b}
                        </li>
                      ))}
                    </ul>
                    <div className="flex items-center justify-between" style={{ marginTop:12 }}>
                      <div style={{ fontSize:12, color: secondary }}>Теги: {tool.tags.join(", ")}</div>
                      <Button onClick={()=>openTool(tool.id, tool.pro)}>Открыть <ChevronRight size={16} style={{marginLeft:6}}/></Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {filtered.length === 0 && !loading && (
              <div style={{ marginTop: 16, fontSize: 14, color: secondary }}>
                Ничего не найдено. Попробуйте другой запрос или категорию.
              </div>
            )}
          </div>
        </section>

        <section id="how" className="section">
          <div className="container">
            <h2>Как это работает</h2>
            <div
              className="grid"
              style={{
                gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
                gap: 24,
                marginTop: 24,
              }}
            >
              {content.how.steps.map((s, index) => (
                <Card key={s.title}>
                  <CardContent>
                    <div
                      style={{
                        width: 40,
                        height: 40,
                        borderRadius: 12,
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        background: "#F3F4F6",
                        color: accent,
                      }}
                    >
                      {s.icon}
                    </div>
                    <h3 style={{ marginTop: 12, fontSize: 20, fontWeight: 500 }}>
                      {index + 1}. {s.title}
                    </h3>
                    <p style={{ marginTop: 6, fontSize: 14, color: secondary }}>{s.desc}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
            <p style={{ marginTop: 16, fontSize: 14, color: secondary }}>{content.how.why}</p>
          </div>
        </section>

        <section className="section">
          <div className="container">
            <h2>Преимущества</h2>
            <div
              className="grid"
              style={{
                gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
                gap: 24,
                marginTop: 16,
              }}
            >
              {content.benefits.map((b) => (
                <Card key={b.title}>
                  <CardContent>
                    <div
                      style={{
                        display: "inline-flex",
                        alignItems: "center",
                        gap: 8,
                        fontSize: 14,
                        color: accent,
                      }}
                    >
                      {b.icon}
                      <span style={{ color: text, fontWeight: 500 }}>{b.title}</span>
                    </div>
                    <p style={{ marginTop: 8, fontSize: 14, color: secondary }}>{b.desc}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>

        <section id="pricing" className="section">
          <div className="container">
            <div className="flex items-center justify-between wrap gap-6">
              <div>
                <h2>Подписка</h2>
                <p style={{ color: secondary, marginTop: 4, fontSize: 14 }}>
                  Free vs Pro {content.pricing.pro}
                  {content.pricing.currency} — триал {content.pricing.trial} дней
                </p>
              </div>
              <div className="flex items-center gap-6">
                <span style={{ fontSize: 14, color: secondary }}>Месяц</span>
                <Switch
                  checked={yearly}
                  onCheckedChange={setYearly}
                  aria-label="Переключить на годовой тариф"
                />
                <span style={{ fontSize: 14, color: secondary }}>Год −25%</span>
              </div>
            </div>

            <div
              className="grid"
              style={{
                gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
                gap: 24,
                marginTop: 24,
              }}
            >
              <Card>
                <CardHeader>
                  <CardTitle>Free</CardTitle>
                  <CardDescription style={{ color: secondary }}>Для разовых задач</CardDescription>
                </CardHeader>
                <CardContent>
                  <ul style={{ fontSize: 14, color: secondary, display: "grid", gap: 8 }}>
                    <li style={{ display: "flex", gap: 8 }}>
                      <Check size={16} color={accent} />
                      До 3 операций/день
                    </li>
                    <li style={{ display: "flex", gap: 8 }}>
                      <Check size={16} color={accent} />
                      Файлы до 10 МБ
                    </li>
                    <li style={{ display: "flex", gap: 8 }}>
                      <Check size={16} color={accent} />
                      Базовые инструменты
                    </li>
                  </ul>
                  <div style={{ marginTop: 12 }}>
                    <Button
                      variant="outline"
                      onClick={() => {
                        track("pricing_cta_click", { plan: "free" });
                        setSigninOpen(true);
                      }}
                    >
                      Начать бесплатно
                    </Button>
                  </div>
                </CardContent>
              </Card>

              <Card style={{ borderColor: accent, borderWidth: 2 }}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle>Pro</CardTitle>
                      <CardDescription style={{ color: secondary }}>
                        Для регулярной работы
                      </CardDescription>
                    </div>
                    <Badge style={{ background: accent, color: "#fff" }}>Рекомендуем</Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="flex items-end" style={{ gap: 8 }}>
                    <div style={{ fontSize: 32, fontWeight: 600 }}>
                      {yearly ? priceMonthYearly : priceMonth}
                    </div>
                    <div style={{ paddingBottom: 2, fontSize: 14, color: secondary }}>
                      {content.pricing.currency}
                    </div>
                  </div>
                  {yearly && (
                    <div style={{ fontSize: 12, marginTop: 4, color: secondary }}>
                      Оплата раз в год: {(priceMonthYearly * 12).toFixed(0)} ₽
                    </div>
                  )}
                  <ul
                    style={{
                      fontSize: 14,
                      color: secondary,
                      display: "grid",
                      gap: 8,
                      marginTop: 12,
                    }}
                  >
                    <li style={{ display: "flex", gap: 8 }}>
                      <Check size={16} color={accent} />
                      Безлимитные операции*
                    </li>
                    <li style={{ display: "flex", gap: 8 }}>
                      <Check size={16} color={accent} />
                      Batch-режим
                    </li>
                    <li style={{ display: "flex", gap: 8 }}>
                      <Check size={16} color={accent} />
                      История и пресеты
                    </li>
                    <li style={{ display: "flex", gap: 8 }}>
                      <Check size={16} color={accent} />
                      Приоритетная очередь
                    </li>
                  </ul>
                  <div style={{ marginTop: 16 }}>
                    <Button
                      onClick={() => {
                        track("pricing_cta_click", { plan: "pro", yearly });
                        setPaywallOpen(true);
                      }}
                    >
                      Начать {content.pricing.trial}-дневный триал{" "}
                      <CreditCard size={16} style={{ marginLeft: 8 }} />
                    </Button>
                    <p style={{ marginTop: 8, fontSize: 12, color: secondary }}>
                      Можно отменить в любой момент.
                    </p>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>

        <section className="section">
          <div className="container">
            <div className="flex items-start gap-6" style={{ padding: 16 }}>
              <div
                style={{
                  width: 40,
                  height: 40,
                  borderRadius: 12,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  background: "#F3F4F6",
                  color: accent,
                }}
              >
                <Lock size={20} />
              </div>
              <div style={{ flex: 1 }}>
                <h3 style={{ fontSize: 20, fontWeight: 500 }}>Приватность и безопасность</h3>
                <p style={{ fontSize: 14, marginTop: 4, color: secondary }}>
                  Файлы обрабатываются локально, где это возможно. Серверные операции — с
                  авто-удалением.
                </p>
                <a
                  href="#"
                  style={{
                    display: "inline-flex",
                    alignItems: "center",
                    gap: 6,
                    fontSize: 14,
                    marginTop: 8,
                    color: accent,
                  }}
                >
                  Подробнее о приватности <ExternalLink size={16} />
                </a>
              </div>
            </div>
          </div>
        </section>

        <section className="section">
          <div className="container">
            <div className="grid" style={{ gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))", gap: 24 }}>
              <div className="card" style={{ padding: 24 }}>
                <h2>Апдейты и бета-фичи</h2>
                <p style={{ color: secondary, marginTop: 8, fontSize: 14, lineHeight: 1.5 }}>
                  Подпишитесь на короткую рассылку: делимся новыми инструментами, приглашаем в бета-тесты и
                  отправляем подсказки по автоматизации. Только по делу.
                </p>
                <ul style={{ marginTop: 12, color: secondary, fontSize: 14, lineHeight: 1.6 }}>
                  <li>✓ Анонсы свежих утилит и улучшений UX.</li>
                  <li>✓ Ранний доступ к бета-функциям и опросам.</li>
                  <li>✓ Кейсы пользователей с готовыми рецептами.</li>
                </ul>
              </div>
              {newsletterEnabled ? (
                <NewsletterForm />
              ) : (
                <Card className="card" style={{ padding: 24 }}>
                  <CardHeader>
                    <CardTitle>Рассылка приостановлена</CardTitle>
                    <CardDescription>
                      Фича отключена фичефлагом. Мы обновим блок после проверки метрик или включим его по вашему домену.
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    {featureFlagsLoading ? (
                      <div className="grid gap-3">
                        <Skeleton className="h-10 w-full" />
                        <Skeleton className="h-10 w-full" />
                        <Skeleton className="h-10 w-full" />
                      </div>
                    ) : (
                      <p style={{ color: secondary, fontSize: 14 }}>
                        Проверьте конфигурацию флага newsletter_form или включите его в админке, чтобы снова собирать лиды.
                      </p>
                    )}
                  </CardContent>
                </Card>
              )}
            </div>
          </div>
        </section>

        <section id="contact" className="section">
          <div className="container">
            <div className="grid" style={{ gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))", gap: 24 }}>
              <div className="card" style={{ padding: 24 }}>
                <h2>Нужен подбор инструментов?</h2>
                <p style={{ color: secondary, marginTop: 8, fontSize: 14, lineHeight: 1.5 }}>
                  Опишите задачу: подготовка презентаций, массовая обработка изображений, автоматизация отчётов из Excel.
                  Ответим в течение рабочего дня и покажем, как закрыть кейс в ProstoKit.
                </p>
                <ul style={{ marginTop: 12, color: secondary, fontSize: 14, lineHeight: 1.6 }}>
                  <li>✓ Пришлём список инструментов под ваш сценарий.</li>
                  <li>✓ Расскажем, как подключить команду и выкатить шаблоны.</li>
                  <li>✓ Дадим 7 дней доступа без ограничений.</li>
                </ul>
              </div>
              {feedbackEnabled ? (
                <FeedbackForm />
              ) : (
                <Card className="card" style={{ padding: 24 }}>
                  <CardHeader>
                    <CardTitle>Форма обратной связи выключена</CardTitle>
                    <CardDescription>Сбор заявок временно недоступен. Проверьте фичефлаг feedback_form.</CardDescription>
                  </CardHeader>
                  <CardContent>
                    {featureFlagsLoading ? (
                      <Skeleton className="h-32 w-full" />
                    ) : (
                      <div className="flex flex-col gap-2 text-sm" style={{ color: secondary }}>
                        <p>Мы продолжаем принимать запросы через support@prostokit.io.</p>
                        <p>Как только флаг будет включен, форма автоматически вернётся на страницу без релиза фронтенда.</p>
                      </div>
                    )}
                  </CardContent>
                </Card>
              )}
            </div>
          </div>
        </section>

        <section id="faq" className="section">
          <div className="container">
            <h2>FAQ</h2>
            <Accordion type="single" collapsible className="">
              {content.faq.map((f) => (
                <AccordionItem key={f.q} value={`item-${f.q}`} className="">
                  <AccordionTrigger data-parent={`item-${f.q}`} className="">
                    {f.q}
                  </AccordionTrigger>
                  <AccordionContent>
                    <p style={{ fontSize: 14, color: secondary }}>{f.a}</p>
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </div>
        </section>

        <section className="section">
          <div className="container">
            <div
              className="card"
              style={{
                border: "1px solid var(--border)",
                borderRadius: 16,
                padding: 24,
                display: "flex",
                gap: 16,
                alignItems: "center",
                justifyContent: "space-between",
                flexWrap: "wrap",
              }}
            >
              <div>
                <h3 style={{ fontSize: 24, fontWeight: 600 }}>{content.tagline}</h3>
                <p style={{ fontSize: 14, marginTop: 4, color: secondary }}>
                  Одна подписка — десятки утилит. Без рекламы.
                </p>
              </div>
              <div className="flex gap-6">
                <Button onClick={onHeroPrimary}>Начать триал</Button>
                <Button variant="outline" onClick={onHeroSecondary}>
                  Открыть каталог
                </Button>
              </div>
            </div>
          </div>
        </section>

        <footer className="section">
          <div className="container">
            <div
              className="grid"
              style={{ gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))", gap: 24 }}
            >
              <div>
                <div className="flex items-center gap-6" style={{ marginBottom: 12 }}>
                  <div
                    style={{
                      width: 32,
                      height: 32,
                      borderRadius: 12,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      background: accent,
                    }}
                  >
                    <Sparkles size={16} color="#fff" />
                  </div>
                  <span style={{ fontWeight: 600 }}>{content.brand}</span>
                </div>
                <p style={{ color: secondary }}>Онлайн-утилиты в один клик.</p>
              </div>
              <div>
                <h4 style={{ fontWeight: 500, marginBottom: 12 }}>Продукт</h4>
                <ul style={{ display: "grid", gap: 8, color: secondary }}>
                  <li>
                    <a href="#catalog">Инструменты</a>
                  </li>
                  <li>
                    <a href="#pricing">Цены</a>
                  </li>
                  <li>
                    <a href="#">Обновления</a>
                  </li>
                </ul>
              </div>
              <div>
                <h4 style={{ fontWeight: 500, marginBottom: 12 }}>Компания</h4>
                <ul style={{ display: "grid", gap: 8, color: secondary }}>
                  <li>
                    <a href="#">О нас</a>
                  </li>
                  <li>
                    <a href="#">Контакты</a>
                  </li>
                </ul>
              </div>
              <div>
                <h4 style={{ fontWeight: 500, marginBottom: 12 }}>Правовые</h4>
                <ul style={{ display: "grid", gap: 8, color: secondary }}>
                  <li>
                    <a href="#">Политика</a>
                  </li>
                  <li>
                    <a href="#">Условия</a>
                  </li>
                </ul>
              </div>
            </div>
            <div className="separator" style={{ margin: "24px 0" }} />
            <div style={{ fontSize: 12, color: secondary }}>
              © {new Date().getFullYear()} {content.brand}. Все права защищены.
            </div>

            <div className="card" style={{ marginTop: 24 }}>
              <div className="card-body">
                <h4 style={{ fontWeight: 500, marginBottom: 8 }}>Как править</h4>
                <ul style={{ fontSize: 14, color: secondary }}>
                  <li>
                    Тексты — объект <code>content</code> в начале файла.
                  </li>
                  <li>
                    Цвета — объект <code>TOKENS</code> (акцент:{" "}
                    <span style={{ color: accent }}>{accent}</span>).
                  </li>
                  <li>
                    Каталог — массив <code>TOOLS</code>.
                  </li>
                  <li>
                    События — <code>track(event, payload)</code>.
                  </li>
                </ul>
                <DevTests priceMonth={priceMonth} />
              </div>
            </div>
          </div>
        </footer>

        <Dialog open={signinOpen} onOpenChange={setSigninOpen}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Вход</DialogTitle>
              <DialogDescription>Доступ к истории и пресетам после входа.</DialogDescription>
            </DialogHeader>
            <div className="card-body">
              <div style={{ display: "grid", gap: 8 }}>
                <Label htmlFor="email">Email</Label>
                <Input id="email" placeholder="you@example.com" type="email" />
                <Label htmlFor="pwd">Пароль</Label>
                <Input id="pwd" placeholder="••••••••" type="password" />
              </div>
            </div>
            <DialogFooter>
              <Button variant="ghost" onClick={() => setSigninOpen(false)}>
                Отмена
              </Button>
              <Button
                onClick={() => {
                  setSigninOpen(false);
                  setToastMsg("Вход выполнен (демо)");
                }}
              >
                Войти
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>

        <Dialog open={paywallOpen} onOpenChange={setPaywallOpen}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Pro-возможности</DialogTitle>
              <DialogDescription>Оформите триал, чтобы открыть Pro-инструменты.</DialogDescription>
            </DialogHeader>
            <div className="card-body" style={{ fontSize: 14, color: secondary }}>
              <ul style={{ paddingLeft: 16, display: "grid", gap: 6 }}>
                <li>
                  7 дней бесплатно, затем {priceMonth}
                  {content.pricing.currency}
                </li>
                <li>Отмена в любой момент</li>
                <li>Batch, история, пресеты</li>
              </ul>
            </div>
            <DialogFooter>
              <Button variant="ghost" onClick={() => setPaywallOpen(false)}>
                Позже
              </Button>
              <Button
                onClick={() => {
                  setPaywallOpen(false);
                  setSigninOpen(true);
                }}
              >
                Начать триал
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>

        {toastMsg && <Toast message={toastMsg} onClose={() => setToastMsg(null)} />}
      </div>
    </TooltipProvider>
  );
}
