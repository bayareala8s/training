const STORAGE_KEY = "baylearn-eia-progress-v1";

function emptyProgress() {
  return {
    lessons: {},
    labs: {},
    challenges: {},
    capstones: {},
    assessment: false,
    learnerName: "",
  };
}

function loadProgress() {
  try {
    return { ...emptyProgress(), ...JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}") };
  } catch {
    return emptyProgress();
  }
}

function saveProgress(p) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(p));
}

function mark(kind, id) {
  const p = loadProgress();
  p[kind][id] = true;
  saveProgress(p);
  return p;
}

function counts() {
  const p = loadProgress();
  const catalog = window.EIA_CATALOG || { modules: [], lessonCount: 0, moduleCount: 15 };
  const lessonTotal = catalog.lessonCount || catalog.modules.reduce((n, m) => n + m.lessons.length, 0);
  const lessonsDone = Object.keys(p.lessons).filter((k) => p.lessons[k]).length;
  const labsTotal = 12;
  const labsDone = Object.keys(p.labs).filter((k) => p.labs[k]).length;
  const chalTotal = (window.EIA_CHALLENGES || []).length;
  const chalDone = Object.keys(p.challenges).filter((k) => p.challenges[k]).length;
  const capTotal = 4;
  const capDone = Object.keys(p.capstones).filter((k) => p.capstones[k]).length;
  const modulesDone = (catalog.modules || []).filter((m) =>
    m.lessons.every((l) => p.lessons[l.id])
  ).length;
  const pct = Math.round(
    ((lessonsDone / Math.max(lessonTotal, 1)) * 0.45 +
      (labsDone / labsTotal) * 0.2 +
      (chalDone / Math.max(chalTotal, 1)) * 0.15 +
      (capDone / capTotal) * 0.15 +
      (p.assessment ? 0.05 : 0)) *
      100
  );
  return {
    p,
    lessonTotal,
    lessonsDone,
    labsTotal,
    labsDone,
    chalTotal,
    chalDone,
    capTotal,
    capDone,
    modulesDone,
    moduleTotal: catalog.moduleCount || 15,
    pct: Math.min(100, pct),
  };
}

function certificateEligible() {
  const c = counts();
  return (
    c.modulesDone >= c.moduleTotal &&
    c.labsDone >= c.labsTotal &&
    c.chalDone >= c.chalTotal &&
    c.capDone >= c.capTotal &&
    c.p.assessment
  );
}

window.EIA_PROGRESS = { loadProgress, saveProgress, mark, counts, certificateEligible, emptyProgress };
