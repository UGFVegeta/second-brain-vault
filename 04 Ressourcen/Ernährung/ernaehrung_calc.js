// Gemeinsame Budget-Rechnung für Tracker und Lebens-Dashboard.
// Ausgleich: Überschuss der letzten 7 Tage (nur Tage mit Einträgen) wird auf 7 Tage verteilt,
// höchstens cap kcal pro Tag, und das Tagesbudget bleibt über dem Mindestwert.
window.ernBudget = function (D, key) {
  const S = D.settings, DAY = 864e5, t = k => new Date(k + "T12:00:00").getTime();
  const iso = d => d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
  const wOf = k => { let w = S.start_weight; for (const [d, x] of Object.entries(D.days).filter(([, v]) => v.weight).sort()) if (d <= k) w = x.weight; return w; };
  const raw = k => {
    const day = D.days[k] || {}, w = wOf(k);
    const bmr = 10 * w + 6.25 * S.height_cm - 5 * S.age + (S.sex === "m" ? 5 : -161);
    const base = Math.round(bmr * S.activity_factor), train = Math.round((day.training_kcal || 0) * S.training_factor);
    return { bmr: Math.round(bmr), base, train, total: base + train - S.deficit };
  };
  const eaten = k => ((D.days[k] || {}).meals || []).reduce((a, m) => a + m.kcal, 0);
  let over = 0;
  for (let i = 1; i <= 7; i++) {
    const k = iso(new Date(t(key) - i * DAY));
    if (eaten(k) > 0) over += eaten(k) - raw(k).total;
  }
  const r = raw(key);
  const cap = S.carry_cap ?? 300, floor = S.min_kcal ?? 1500;
  let adj = Math.max(0, Math.min(cap, Math.round(over / 7)));
  adj = Math.max(0, Math.min(adj, r.total - floor));
  return { ...r, adj, total: r.total - adj, eaten: eaten(key), over };
};
