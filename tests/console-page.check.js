// Offline check of templates/console-page.html against tests/fixtures/ledger.
// Synthetic data only. Needs: npm i playwright, and a Chromium (PW_CHROMIUM or Playwright's own).
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const root = path.resolve(__dirname, "..");
const page = "file://" + path.join(root, "templates", "console-page.html");
const fixtures = path.join(__dirname, "fixtures", "ledger");

function loadFixtures() {
  const data = {};
  for (const col of fs.readdirSync(fixtures)) {
    for (const f of fs.readdirSync(path.join(fixtures, col))) {
      const id = f.replace(/\.json$/, "");
      const row = JSON.parse(fs.readFileSync(path.join(fixtures, col, f), "utf8"));
      (data[col] ||= []).push({ id, ...row });
    }
  }
  return data;
}

async function run(browser, name, opts, data) {
  const p = await browser.newPage(opts);
  const errors = [];
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
  if (data) {
    await p.addInitScript((data) => {
      const snap = (id, d) => ({ id, exists: !!d, data: () => d, metadata: {} });
      const query = (name) => {
        let field = null, dir = "asc", lim = 1000;
        const q = {
          orderBy(f, d) { field = f; dir = d || "asc"; return q; },
          limit(n) { lim = n; return q; },
          onSnapshot(next) {
            setTimeout(() => {
              let docs = (data[name] || []).slice();
              if (field) docs.sort((a, b) => (a[field] > b[field] ? 1 : -1) * (dir === "desc" ? -1 : 1));
              docs = docs.slice(0, lim).map((d) => snap(d.id, d));
              next({ docs, size: docs.length, empty: !docs.length });
            }, 30);
            return () => {};
          },
        };
        return q;
      };
      window.claude = {
        use: async (n) => n === "db"
          ? { doc: (p) => ({ onSnapshot(next) { const [c, id] = p.split("/"); const d = (data[c] || []).find((r) => r.id === id); setTimeout(() => next(snap(id, d)), 30); return () => {}; } }), collection: query }
          : null,
      };
    }, data);
  }
  await p.goto(page);
  await p.waitForTimeout(400);
  const result = await p.evaluate(() => ({
    scrollWidth: document.documentElement.scrollWidth,
    registry: !!document.querySelector("#registry table"),
    tasks: !!document.querySelector("#tasks ul"),
    events: !!document.querySelector("#events ul"),
    findings: !!document.querySelector("#findings table"),
    emptyStates: document.querySelectorAll(".empty").length,
  }));
  console.log(name, JSON.stringify({ errors: errors.length, ...result }));
  await p.close();
  return errors.length === 0 && result.scrollWidth <= opts.viewport.width;
}

(async () => {
  const launch = process.env.PW_CHROMIUM ? { executablePath: process.env.PW_CHROMIUM } : {};
  const b = await chromium.launch(launch);
  let ok = true;
  ok &= await run(b, "wide", { viewport: { width: 1200, height: 1200 }, colorScheme: "light" });
  ok &= await run(b, "phone", { viewport: { width: 390, height: 1200 }, colorScheme: "dark" });
  ok &= await run(b, "seeded", { viewport: { width: 1200, height: 1600 } }, loadFixtures());
  await b.close();
  process.exit(ok ? 0 : 1);
})();
