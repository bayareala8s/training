/* BayLearn EIA course player */
const $ = (sel) => document.querySelector(sel);

function pathOf() {
  const h = location.hash.replace(/^#/, "") || "/";
  return h.startsWith("/") ? h : "/" + h;
}

async function mdToHtml(md) {
  if (window.marked) {
    window.marked.setOptions({ mangle: false, headerIds: true });
    return window.marked.parse(md);
  }
  return "<pre>" + md.replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c])) + "</pre>";
}

async function fetchText(rel) {
  const url = new URL("../" + rel.replace(/^\.\.\//, ""), window.location.href);
  const res = await fetch(url);
  if (!res.ok) throw new Error("Could not load " + rel + " (start python3 -m http.server from the repo root)");
  return res.text();
}

function setActiveNav(route) {
  document.querySelectorAll(".ba-nav a").forEach((a) => {
    a.classList.toggle("active", a.getAttribute("href") === "#" + route || (route === "/" && a.dataset.home));
  });
}

function renderLanding() {
  return `
  <section class="ba-hero">
    <div class="wrap">
      <div class="badges">
        <span class="badge gold">Advanced</span>
        <span class="badge">Hands-On Labs</span>
        <span class="badge">Architecture Challenges</span>
        <span class="badge">4 Capstone Projects</span>
        <span class="badge">AWS</span>
        <span class="badge">Terraform</span>
        <span class="badge">AI Agents</span>
        <span class="badge">Enterprise Architecture</span>
      </div>
      <h1>Enterprise Integration Architecture</h1>
      <p class="sub"><strong>Master APIs, Messaging, Events, File Transfers, ESB Modernization &amp; AI-Agent Integration through Real-World Enterprise Architecture Labs.</strong></p>
      <p class="sub" style="margin-top:1rem">Do not start with an AWS service. Start with the integration requirement.</p>
      <div class="actions">
        <a class="btn gold" href="#/start">Start here</a>
        <a class="btn ghost" href="#/learn/1.1">Lesson 1.1</a>
        <a class="btn ghost" href="#/dashboard">Dashboard</a>
      </div>
    </div>
  </section>
  <div class="wrap">
    <div class="grid">
      <div class="card"><h3>Decision framework</h3><p>API vs Message vs Event vs File vs ESB vs AI Agent — used in every module, lab, and capstone.</p></div>
      <div class="card"><h3>Failure-first labs</h3><p>Poison messages, duplicate files, IAM holes, timeouts — diagnose, fix, replay.</p></div>
      <div class="card"><h3>Portfolio capstones</h3><p>Banking, commerce, healthcare, and global supply chain platforms with ADRs.</p></div>
      <div class="card"><h3>Governed agents</h3><p>User → Agent → Tool → Integration layer → System. Never LLM → production database.</p></div>
    </div>
    <p class="muted" style="margin-top:1.5rem">Offered by BayAreaLa8s · BayLearn Academy. 15 modules · 128 lessons · 12 labs · 25 architecture challenges.</p>
  </div>`;
}

function renderDashboard() {
  const c = EIA_PROGRESS.counts();
  const bar = "█".repeat(Math.round(c.pct / 5)) + "░".repeat(20 - Math.round(c.pct / 5));
  const modules = (EIA_CATALOG.modules || [])
    .map((m) => {
      const done = m.lessons.filter((l) => c.p.lessons[l.id]).length;
      return `<div class="card">
        <h3>Module ${m.id}. ${m.title}</h3>
        <p>${done} / ${m.lessons.length} lessons${m.lab ? " · lab " + m.lab : ""}</p>
        <p style="margin-top:0.6rem"><a class="btn" href="#/module/${m.id}">Open</a></p>
      </div>`;
    })
    .join("");
  return `<div class="wrap">
    <h1>Course dashboard</h1>
    <div class="card" style="margin-bottom:1rem">
      <div class="bar-label"><span>Course progress</span><span class="stat">${c.pct}%</span></div>
      <div class="progress-track"><div class="progress-fill" style="width:${c.pct}%"></div></div>
      <pre style="margin:0.8rem 0 0;background:#0a1f33;color:#d6eaf1;padding:0.8rem;border-radius:4px">Course Progress
${bar} ${c.pct}%

Modules Completed: ${c.modulesDone} / ${c.moduleTotal}
Labs Completed: ${c.labsDone} / ${c.labsTotal}
Capstones: ${c.capDone} / ${c.capTotal}
Architecture Challenges: ${c.chalDone} / ${c.chalTotal}</pre>
    </div>
    <div class="grid">
      <div class="card"><h3>Labs</h3><p>12 workbooks with Terraform, failure tests, and cleanup.</p><p style="margin-top:0.6rem"><a href="#/labs">Open labs</a></p></div>
      <div class="card"><h3>Challenges</h3><p>25 architecture decisions with written rationale.</p><p style="margin-top:0.6rem"><a href="#/challenges">Open challenges</a></p></div>
      <div class="card"><h3>Capstones</h3><p>Four portfolio platforms.</p><p style="margin-top:0.6rem"><a href="#/capstones">Open capstones</a></p></div>
      <div class="card"><h3>Certificate</h3><p>Earn the BayLearn Certificate of Completion.</p><p style="margin-top:0.6rem"><a href="#/certificate">View certificate</a></p></div>
    </div>
    <h2>Modules</h2>
    <div class="grid">${modules}</div>
  </div>`;
}

function sidebar(currentLesson) {
  const p = EIA_PROGRESS.loadProgress();
  const items = (EIA_CATALOG.modules || [])
    .map((m) => {
      const ls = m.lessons
        .map((l) => {
          const mark = p.lessons[l.id] ? "✓ " : "";
          const cls = l.id === currentLesson ? "active" : "";
          return `<a class="${cls}" href="#/learn/${l.id}">${mark}${l.id} ${l.title}</a>`;
        })
        .join("");
      return `<div style="margin-bottom:0.7rem"><strong style="font-size:0.8rem">M${m.id} ${m.title}</strong>${ls}</div>`;
    })
    .join("");
  return `<aside class="sidebar"><h2>Modules</h2>${items}</aside>`;
}

async function renderStart() {
  try {
    const html = await mdToHtml(await fetchText("GETTING_STARTED.md"));
    return `<div class="wrap"><article class="lesson markdown-body">${html}
      <div class="actions">
        <a class="btn gold" href="#/learn/1.1">Begin Lesson 1.1</a>
        <a class="btn" href="#/lab/lab-01-classification">Open Lab 1</a>
      </div></article></div>`;
  } catch (e) {
    return `<div class="wrap"><p class="feedback bad">${e.message}</p>
      <p>From the repository root run <code>./scripts/start_course.sh</code> then open <code>/course-ui/</code>.</p></div>`;
  }
}

async function renderLesson(id) {
  let found = null;
  let mod = null;
  for (const m of EIA_CATALOG.modules || []) {
    const l = m.lessons.find((x) => x.id === id);
    if (l) {
      found = l;
      mod = m;
      break;
    }
  }
  if (!found) return `<div class="wrap"><p>Lesson ${id} not found.</p></div>`;
  let html;
  try {
    const md = await fetchText(found.path);
    html = await mdToHtml(md);
  } catch (e) {
    html = `<p class="feedback bad">${e.message}</p>`;
  }
  const idx = mod.lessons.findIndex((l) => l.id === id);
  const prev = mod.lessons[idx - 1];
  const next = mod.lessons[idx + 1] || null;
  const nextMod = !next
    ? EIA_CATALOG.modules[EIA_CATALOG.modules.findIndex((m) => m.id === mod.id) + 1]
    : null;
  const nextHref = next
    ? `#/learn/${next.id}`
    : nextMod
      ? `#/learn/${nextMod.lessons[0].id}`
      : "#/dashboard";
  return `<div class="wrap layout">
    ${sidebar(id)}
    <article class="lesson markdown-body">
      ${html}
      <div class="actions">
        <button class="btn" id="complete-lesson">Mark lesson complete</button>
        ${prev ? `<a class="btn ghost" style="color:var(--ba-navy);border-color:var(--ba-border)" href="#/learn/${prev.id}">Previous</a>` : ""}
        <a class="btn gold" href="${nextHref}">Next</a>
      </div>
    </article>
  </div>`;
}

function renderModule(id) {
  const m = (EIA_CATALOG.modules || []).find((x) => x.id === id || Number(x.id) === Number(id));
  if (!m) return `<div class="wrap"><p>Module not found.</p></div>`;
  const p = EIA_PROGRESS.loadProgress();
  const lis = m.lessons
    .map(
      (l) =>
        `<li>${p.lessons[l.id] ? "✓ " : ""}<a href="#/learn/${l.id}">${l.id} — ${l.title}</a></li>`
    )
    .join("");
  return `<div class="wrap">
    <h1>Module ${m.id} — ${m.title}</h1>
    <ul>${lis}</ul>
    ${m.lab ? `<p><a class="btn" href="#/lab/${m.lab}">Open lab</a></p>` : ""}
  </div>`;
}

const LAB_INDEX = [
  ["lab-01-classification", "Lab 1 — Integration architecture classification", "No AWS"],
  ["lab-02-api", "Lab 2 — API Gateway → Lambda → DynamoDB", "~$0.10 if destroyed"],
  ["lab-03-messaging", "Lab 3 — SQS, DLQ, replay", "~$0.10"],
  ["lab-04-pubsub", "Lab 4 — SNS fan-out", "~$0.10"],
  ["lab-05-events", "Lab 5 — EventBridge choreography", "~$0.15"],
  ["lab-06-file-transfer", "Lab 6 — File landing + catalog (Transfer optional)", "Keep Transfer OFF"],
  ["lab-07-large-files", "Lab 7 — Direct S3 upload + status", "~$0.15"],
  ["lab-08-esb-modernization", "Lab 8 — ESB strangler + ADR", "No AWS required"],
  ["lab-11-chaos", "Lab 11 — Chaos (poison, invalid JSON, DLQ)", "Dedicated stack"],
  ["lab-12-security", "Security lab — fix the insecure architecture", "~$0.10"],
  ["lab-13-observability", "Observability — operations dashboard", "~$0.10"],
  ["lab-15-ai-agent", "AI lab — operations agent + HITL", "Bedrock optional"],
];

function renderLabs() {
  const p = EIA_PROGRESS.loadProgress();
  const rows = LAB_INDEX.map(
    ([id, title, cost]) => `<div class="card">
      <h3>${p.labs[id] ? "✓ " : ""}${title}</h3>
      <p>${cost}</p>
      <p style="margin-top:0.6rem"><a class="btn" href="#/lab/${id}">Open</a></p>
    </div>`
  ).join("");
  return `<div class="wrap"><h1>Labs</h1><p class="muted">Every AWS lab supports terraform destroy. Transfer Family must not stay ONLINE idle.</p><div class="grid">${rows}</div></div>`;
}

async function renderLab(id) {
  let html;
  try {
    const md = await fetchText("labs/" + id + "/README.md");
    html = await mdToHtml(md);
  } catch (e) {
    html = `<p>Workbook: <code>labs/${id}/README.md</code></p><p class="muted">${e.message}</p>`;
  }
  return `<div class="wrap"><article class="lesson">${html}
    <div class="actions"><button class="btn" id="complete-lab" data-lab="${id}">Mark lab complete</button>
    <a class="btn gold" href="#/labs">All labs</a></div></article></div>`;
}

function renderChallenges() {
  const p = EIA_PROGRESS.loadProgress();
  const items = EIA_CHALLENGES.map((ch) => {
    const done = p.challenges[ch.id];
    return `<div class="card" id="${ch.id}">
      <h3>${done ? "✓ " : ""}${ch.id.toUpperCase()} · Module ${ch.module} · ${ch.title}</h3>
      <p>${ch.scenario}</p>
      <form data-chal="${ch.id}">
        ${ch.options.map((o) => `<label class="choice"><input type="radio" name="ans" value="${o.id}"> ${o.id}. ${o.label}</label>`).join("")}
        <label class="muted" style="display:block;margin-top:0.6rem">Explain your decision (required)</label>
        <textarea name="why" rows="3" style="width:100%;margin:0.35rem 0;font-family:inherit"></textarea>
        <button class="btn" type="submit">Submit</button>
        <div class="feedback hidden" data-fb></div>
      </form>
    </div>`;
  }).join("");
  return `<div class="wrap"><h1>Architecture challenges</h1>
    <p>Do not merely pick the letter. The explanation is the work. Correct letters without rationale are incomplete.</p>
    <div class="grid" style="grid-template-columns:1fr">${items}</div></div>`;
}

const CAPSTONES = [
  ["banking", "Enterprise Payment Integration Platform", "Banking"],
  ["ecommerce", "Event-Driven Commerce Platform", "Retail / e-commerce"],
  ["healthcare", "Secure Healthcare Integration Platform", "Healthcare"],
  ["manufacturing", "Global Supply Chain Integration Platform", "Manufacturing"],
];

function renderCapstones() {
  const p = EIA_PROGRESS.loadProgress();
  const cards = CAPSTONES.map(
    ([id, title, domain]) => `<div class="card">
      <h3>${p.capstones[id] ? "✓ " : ""}${title}</h3>
      <p>${domain}. Design first — the brief does not hand you the final architecture.</p>
      <p style="margin-top:0.6rem"><a class="btn" href="#/capstone/${id}">Open brief</a></p>
    </div>`
  ).join("");
  return `<div class="wrap"><h1>Capstones</h1><p class="muted">Portfolio-ready: diagram, ADRs, Terraform, tests, security, observability.</p><div class="grid">${cards}</div>
    <p><a href="#/assessment">Final architecture assessment</a></p></div>`;
}

async function renderCapstone(id) {
  let html;
  try {
    html = await mdToHtml(await fetchText("capstones/" + id + "/README.md"));
  } catch (e) {
    html = `<p>${e.message}</p>`;
  }
  return `<div class="wrap"><article class="lesson">${html}
    <div class="actions"><button class="btn" id="complete-cap" data-cap="${id}">Mark capstone complete</button></div></article></div>`;
}

async function renderAssessment() {
  let html;
  try {
    html = await mdToHtml(await fetchText("assessments/final-architecture-assessment.md"));
  } catch (e) {
    html = `<p>${e.message}</p>`;
  }
  return `<div class="wrap"><article class="lesson">${html}
    <div class="actions"><button class="btn" id="complete-assess">Mark assessment submitted</button></div></article></div>`;
}

function renderCertificate() {
  const ok = EIA_PROGRESS.certificateEligible();
  const p = EIA_PROGRESS.loadProgress();
  const name = p.learnerName || "Learner";
  if (!ok) {
    const c = EIA_PROGRESS.counts();
    return `<div class="wrap">
      <h1>Certificate</h1>
      <p>Complete all required modules, labs, 25 challenges, four capstones, and the final assessment.</p>
      <pre>Modules ${c.modulesDone}/${c.moduleTotal}
Labs ${c.labsDone}/${c.labsTotal}
Challenges ${c.chalDone}/${c.chalTotal}
Capstones ${c.capDone}/${c.capTotal}
Assessment ${c.p.assessment ? "yes" : "no"}</pre>
    </div>`;
  }
  return `<div class="wrap">
    <label class="muted">Name on certificate</label>
    <input id="cert-name" value="${name}" style="padding:0.4rem;margin:0.4rem 0 1rem;width:min(400px,100%)">
    <div class="cert" id="cert-paper">
      <p style="letter-spacing:0.2em;text-transform:uppercase;color:var(--ba-teal)">BayAreaLa8s · BayLearn Academy</p>
      <h1>BayLearn Certificate of Completion</h1>
      <h2 style="color:var(--ba-navy);margin:0.4rem 0 1rem">Enterprise Integration Architecture</h2>
      <p>APIs • Messaging • Events • File Transfers • ESB • AI Agents</p>
      <p style="margin:1.5rem 0;font-size:1.3rem"><strong id="cert-display">${name}</strong></p>
      <p>has completed the required modules, labs, architecture challenges, and four capstone projects.</p>
      <p style="margin-top:2rem;color:var(--ba-slate)">Advanced · Hands-on · Architecture-first</p>
    </div>
    <button class="btn gold" onclick="window.print()">Print / save PDF</button>
  </div>`;
}

async function render() {
  const path = pathOf();
  setActiveNav(path);
  const app = $("#app");
  let view = path;
  if (path === "/") view = renderLanding();
  else if (path === "/start") view = await renderStart();
  else if (path === "/dashboard") view = renderDashboard();
  else if (path.startsWith("/learn/")) view = await renderLesson(path.split("/")[2]);
  else if (path.startsWith("/module/")) view = renderModule(path.split("/")[2]);
  else if (path === "/labs") view = renderLabs();
  else if (path.startsWith("/lab/")) view = await renderLab(path.split("/")[2]);
  else if (path === "/challenges") view = renderChallenges();
  else if (path === "/capstones") view = renderCapstones();
  else if (path.startsWith("/capstone/")) view = await renderCapstone(path.split("/")[2]);
  else if (path === "/assessment") view = await renderAssessment();
  else if (path === "/certificate") view = renderCertificate();
  else view = renderLanding();
  app.innerHTML = view;
  if (window.mermaid) {
    document.querySelectorAll("pre code.language-mermaid, pre.mermaid").forEach((el) => {
      const pre = el.tagName === "CODE" ? el.parentElement : el;
      const div = document.createElement("div");
      div.className = "mermaid";
      div.textContent = el.textContent;
      pre.replaceWith(div);
    });
    try {
      window.mermaid.run({ querySelector: ".mermaid" });
    } catch { /* ignore */ }
  }
  const cl = $("#complete-lesson");
  if (cl) {
    cl.onclick = () => {
      const id = path.split("/")[2];
      EIA_PROGRESS.mark("lessons", id);
      cl.textContent = "Completed";
    };
  }
  const labBtn = $("#complete-lab");
  if (labBtn) labBtn.onclick = () => { EIA_PROGRESS.mark("labs", labBtn.dataset.lab); labBtn.textContent = "Completed"; };
  const capBtn = $("#complete-cap");
  if (capBtn) capBtn.onclick = () => { EIA_PROGRESS.mark("capstones", capBtn.dataset.cap); capBtn.textContent = "Completed"; };
  const as = $("#complete-assess");
  if (as) as.onclick = () => {
    const p = EIA_PROGRESS.loadProgress();
    p.assessment = true;
    EIA_PROGRESS.saveProgress(p);
    as.textContent = "Recorded";
  };
  const name = $("#cert-name");
  if (name) {
    name.oninput = () => {
      const p = EIA_PROGRESS.loadProgress();
      p.learnerName = name.value;
      EIA_PROGRESS.saveProgress(p);
      const d = $("#cert-display");
      if (d) d.textContent = name.value || "Learner";
    };
  }
  document.querySelectorAll("form[data-chal]").forEach((form) => {
    form.onsubmit = (ev) => {
      ev.preventDefault();
      const id = form.dataset.chal;
      const ch = EIA_CHALLENGES.find((x) => x.id === id);
      const ans = (form.ans && form.ans.value) || "";
      const why = (form.why && form.why.value.trim()) || "";
      const fb = form.querySelector("[data-fb]");
      fb.classList.remove("hidden", "ok", "bad");
      if (!ans || why.length < 40) {
        fb.classList.add("bad");
        fb.textContent = "Choose an option and write at least 40 characters of rationale (requirement, characteristics, pattern, rejected options).";
        return;
      }
      const ok = ans === ch.correct;
      fb.classList.add(ok ? "ok" : "bad");
      fb.innerHTML = (ok ? "Directionally correct. " : "Not the best option. ") + ch.explanation +
        (ok ? "" : " Your rationale still matters—revise using NFRs.");
      if (ok && why.length >= 40) EIA_PROGRESS.mark("challenges", id);
    };
  });
}

window.addEventListener("hashchange", render);
window.addEventListener("load", render);
