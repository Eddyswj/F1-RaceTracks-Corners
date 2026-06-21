const tracksData = window.TRACKS_DATA || { tracks: {} };

const trackSelect = document.getElementById("track-select");
const analyzeForm = document.getElementById("analyze-form");
const statusBox = document.getElementById("status");
const predictionCount = document.getElementById("prediction-count");
const eventCount = document.getElementById("event-count");

const trackTitle = document.getElementById("track-title");
const trackUnique = document.getElementById("track-unique");
const trackOverview = document.getElementById("track-overview");
const characteristicsList = document.getElementById("characteristics-list");
const strategyList = document.getElementById("strategy-list");
const overtakingList = document.getElementById("overtaking-list");
const drsList = document.getElementById("drs-list");
const historyList = document.getElementById("history-list");

const trackMap = document.getElementById("track-map");
const sectionTitle = document.getElementById("section-title");
const sectionSignificance = document.getElementById("section-significance");
const sectionFact = document.getElementById("section-fact");

const originalVideo = document.getElementById("original-video");
const annotatedVideo = document.getElementById("annotated-video");
const eventPopup = document.getElementById("event-popup");

let selectedTrackId = "";
let currentEvents = [];
let activeSectionId = "";

function renderBulletList(targetElement, items) {
  targetElement.innerHTML = "";
  (items || []).forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    targetElement.appendChild(li);
  });
}

function setStatus(text, mode = "idle") {
  statusBox.textContent = text;
  statusBox.className = `status ${mode}`;
}

function buildTrackSelect() {
  const entries = Object.entries(tracksData.tracks || {});
  entries.forEach(([id, track]) => {
    const option = document.createElement("option");
    option.value = id;
    option.textContent = track.name;
    trackSelect.appendChild(option);
  });

  if (entries.length > 0) {
    selectedTrackId = entries[0][0];
    trackSelect.value = selectedTrackId;
    renderTrack(selectedTrackId);
  }
}

function findSection(track, sectionId, fallbackLabel = "") {
  if (!track) {
    return null;
  }

  const exact = (track.sections || []).find((s) => s.id === sectionId);
  if (exact) {
    return exact;
  }

  const aliasMatch = (track.sections || []).find((s) => Array.isArray(s.aliases) && s.aliases.includes(sectionId));
  if (aliasMatch) {
    return aliasMatch;
  }

  const normalizedLabel = fallbackLabel.toLowerCase();
  const turnNumber = normalizedLabel.match(/(?:turn|corner)\s*[-_]?\s*(\d+)/);
  if (turnNumber) {
    const turnId = `turn-${turnNumber[1]}`;
    const aliasTurnMatch = (track.sections || []).find((s) => Array.isArray(s.aliases) && s.aliases.includes(turnId));
    return (track.sections || []).find((s) => s.id === turnId) || aliasTurnMatch || null;
  }

  if (normalizedLabel.includes("drs")) {
    return (track.sections || []).find((s) => s.id.startsWith("drs") || s.id.startsWith("drs_")) || null;
  }

  if (normalizedLabel.includes("sector")) {
    const sec = normalizedLabel.match(/sector\s*[-_]?\s*(\d+)/);
    if (sec) {
      const sectorId = `sector-${sec[1]}`;
      const aliasSectorMatch = (track.sections || []).find((s) => Array.isArray(s.aliases) && s.aliases.includes(sectorId));
      return (track.sections || []).find((s) => s.id === sectorId) || aliasSectorMatch || null;
    }
  }

  return null;
}

function renderTrack(trackId) {
  const track = tracksData.tracks?.[trackId];
  if (!track) {
    return;
  }

  selectedTrackId = trackId;
  trackMap.classList.toggle("spa-track-map", trackId === "spa");
  trackMap.style.backgroundImage = trackId === "spa" ? "url('/assets/spa-map')" : "none";
  trackTitle.textContent = track.name;
  trackUnique.textContent = track.unique;
  trackOverview.textContent = track.overview;

  renderBulletList(characteristicsList, track.key_characteristics);
  renderBulletList(strategyList, track.strategy_focus);
  renderBulletList(overtakingList, track.overtaking_hotspots);
  renderBulletList(historyList, track.historical_notes);

  drsList.innerHTML = "";
  (track.drs_zones || []).forEach((drs) => {
    const li = document.createElement("li");
    li.textContent = `${drs.name}: ${drs.detail}`;
    drsList.appendChild(li);
  });

  [...trackMap.querySelectorAll(".section-node")].forEach((n) => n.remove());

  (track.sections || []).forEach((section) => {
    const node = document.createElement("button");
    node.type = "button";
    node.className = "section-node";
    node.style.left = `${section.map.x}%`;
    node.style.top = `${section.map.y}%`;
    node.dataset.sectionId = section.id;
    node.title = section.name;

    node.addEventListener("mouseenter", () => {
      updateSectionPanel(section);
    });

    node.addEventListener("click", () => {
      updateSectionPanel(section);
      setActiveSection(section.id);
    });

    trackMap.appendChild(node);
  });

  const first = track.sections?.[0];
  if (first) {
    updateSectionPanel(first);
    setActiveSection(first.id);
  }
}

function updateSectionPanel(section) {
  sectionTitle.textContent = `${section.name} (${section.type})`;
  sectionSignificance.textContent = section.significance;
  sectionFact.textContent = `Cool detail: ${section.cool_fact}`;
}

function setActiveSection(sectionId) {
  activeSectionId = sectionId;
  [...trackMap.querySelectorAll(".section-node")].forEach((node) => {
    node.classList.toggle("active", node.dataset.sectionId === sectionId);
  });
}

function onVideoTimeUpdate() {
  if (!currentEvents.length || !selectedTrackId) {
    return;
  }

  const track = tracksData.tracks?.[selectedTrackId];
  if (!track) {
    return;
  }

  const currentTime = annotatedVideo.currentTime || originalVideo.currentTime || 0;

  let currentEvent = null;
  for (let i = currentEvents.length - 1; i >= 0; i -= 1) {
    if (currentEvents[i].time <= currentTime) {
      currentEvent = currentEvents[i];
      break;
    }
  }

  if (!currentEvent) {
    return;
  }

  const section = findSection(track, currentEvent.section_id, currentEvent.label);
  if (!section) {
    return;
  }

  if (activeSectionId !== section.id) {
    setActiveSection(section.id);
    updateSectionPanel(section);
    const confidencePct = Math.round((currentEvent.confidence || 0) * 100);
    eventPopup.textContent = `Detected ${currentEvent.label} (${confidencePct}%) -> ${section.name}`;
    eventPopup.classList.remove("hidden");
  }
}

function attachSyncHandlers() {
  originalVideo.addEventListener("timeupdate", onVideoTimeUpdate);
  annotatedVideo.addEventListener("timeupdate", onVideoTimeUpdate);
}

trackSelect.addEventListener("change", (e) => {
  renderTrack(e.target.value);
});

analyzeForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(analyzeForm);
  setStatus("Running Roboflow inference. This can take a bit for longer videos...", "loading");

  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Unknown error while running inference");
    }

    predictionCount.textContent = String(data.prediction_frames || 0);
    eventCount.textContent = String((data.events || []).length);

    currentEvents = (data.events || []).slice().sort((a, b) => a.time - b.time);

    if (data.track && tracksData.tracks?.[data.track]) {
      trackSelect.value = data.track;
      renderTrack(data.track);
    }

    originalVideo.src = data.video_url;
    annotatedVideo.src = data.annotated_video_url;
    eventPopup.classList.add("hidden");

    setStatus("Inference complete. Play either video to see the map auto-highlight sections.", "success");
  } catch (err) {
    setStatus(`Failed: ${err.message}`, "error");
  }
});

buildTrackSelect();
attachSyncHandlers();
