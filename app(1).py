import html
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Motion Lab", page_icon="✨", layout="wide")

st.title("Hello World Motion Lab")
st.caption("A tiny app for experimenting with names, typography, backgrounds, and motion.")

with st.sidebar:
    st.header("Customize your app")
    name = st.text_input("Enter your name", value="Hello World", max_chars=80)
    font_family = st.selectbox(
        "Font type",
        ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana", "Trebuchet MS", "Impact", "Comic Sans MS"],
    )
    font_size = st.slider("Font size", min_value=20, max_value=100, value=48, step=2)
    background = st.selectbox(
        "Background",
        ["Light", "Dark", "Sky", "Sunset", "Mint", "Lavender", "Midnight"],
    )
    name_mode = st.selectbox("Name display mode", ["Centered", "Ticker Tape", "Repeated"])
    effect = st.selectbox(
        "Dynamic action",
        ["None", "Rain", "Snow", "Hail", "Wind gust", "Confetti", "Tornado"],
    )
    speed = st.slider("Animation speed", min_value=1, max_value=10, value=5, help="Higher values move the effects faster.")
    st.divider()
    st.caption("Tip: change a few settings and watch the preview update.")

backgrounds = {
    "Light": ("#f8fafc", "#111827"),
    "Dark": ("#080b12", "#f9fafb"),
    "Sky": ("#cceeff", "#12304a"),
    "Sunset": ("linear-gradient(135deg, #ffb199, #ffecd2)", "#4a2030"),
    "Mint": ("#d9fbe8", "#174b3a"),
    "Lavender": ("linear-gradient(135deg, #e9d5ff, #fce7f3)", "#3b245c"),
    "Midnight": ("linear-gradient(135deg, #101935, #34205c)", "#ffffff"),
}
bg_value, text_color = backgrounds[background]
safe_name = html.escape(name or "Hello World")
# JSON encoding safely passes user text and selected values into the iframe script.
config = {
    "name": name or "Hello World",
    "fontFamily": font_family,
    "fontSize": font_size,
    "background": bg_value,
    "textColor": text_color,
    "mode": name_mode,
    "effect": effect,
    "speed": speed,
}
config_json = json.dumps(config).replace("</", "<\\/")

html_doc = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  * { box-sizing: border-box; }
  html, body { margin: 0; width: 100%; height: 100%; }
  body { font-family: Arial, sans-serif; }
  #stage {
    position: relative; width: 100%; height: 620px; overflow: hidden;
    background: var(--stage-bg); color: var(--text-color);
    border-radius: 18px; isolation: isolate;
  }
  #particles { position: absolute; inset: 0; overflow: hidden; pointer-events: none; }
  .particle { position: absolute; top: -12%; left: 0; user-select: none; will-change: transform; }
  #name-wrap {
    position: absolute; z-index: 2; inset: 0; display: flex;
    align-items: center; justify-content: center; padding: 28px;
    overflow: hidden; font-family: var(--font-family); font-size: var(--font-size);
    font-weight: 700; text-align: center; overflow-wrap: anywhere;
    text-shadow: 0 2px 10px rgba(0,0,0,.10);
  }
  #name-text { max-width: 100%; }
  #name-wrap.repeated { display: block; padding-top: 24px; line-height: 1.5; }
  #name-wrap.ticker { justify-content: flex-start; white-space: nowrap; }
  #name-wrap.ticker #name-text { white-space: nowrap; animation: ticker 12s linear infinite; }
  @keyframes ticker { from { transform: translateX(105%); } to { transform: translateX(-110%); } }
  .hint { position: absolute; bottom: 14px; left: 0; right: 0; z-index: 3; text-align: center;
          font: 12px Arial, sans-serif; opacity: .65; }
  @media (prefers-reduced-motion: reduce) {
    #name-wrap.ticker #name-text { animation-duration: 30s; }
  }
</style>
</head>
<body>
<div id="stage">
  <div id="particles" aria-hidden="true"></div>
  <div id="name-wrap"><div id="name-text"></div></div>
  <div class="hint">HELLO WORLD · MOTION PREVIEW</div>
</div>
<script>
const cfg = __CONFIG__;
const stage = document.getElementById("stage");
const nameWrap = document.getElementById("name-wrap");
const nameText = document.getElementById("name-text");
const particles = document.getElementById("particles");

stage.style.setProperty("--stage-bg", cfg.background);
stage.style.setProperty("--text-color", cfg.textColor);
stage.style.setProperty("--font-family", JSON.stringify(cfg.fontFamily));
stage.style.setProperty("--font-size", cfg.fontSize + "px");
nameText.textContent = cfg.name || "Hello World";
nameWrap.classList.toggle("ticker", cfg.mode === "Ticker Tape");
nameWrap.classList.toggle("repeated", cfg.mode === "Repeated");
if (cfg.mode === "Repeated") {
  nameText.replaceChildren();
  for (let i = 0; i < 7; i++) {
    const line = document.createElement("div");
    line.textContent = cfg.name || "Hello World";
    nameText.appendChild(line);
  }
}

const symbols = {
  "Rain": ["💧", "💦"],
  "Snow": ["❄", "❅", "✻"],
  "Hail": ["🧊", "●"],
  "Wind gust": ["〰", "➜", "💨"],
  "Confetti": ["🎉", "🎊", "✦", "●", "▲", "■"],
  "Tornado": ["🌪", "〰", "·"]
};
const effect = cfg.effect;
const count = effect === "Confetti" ? 75 : effect === "Tornado" ? 42 : 54;
const speedFactor = 1.35 - cfg.speed * 0.105;
const items = [];
function rand(min, max) { return Math.random() * (max - min) + min; }

if (effect !== "None") {
  for (let i = 0; i < count; i++) {
    const el = document.createElement("span");
    el.className = "particle";
    el.textContent = symbols[effect][Math.floor(Math.random() * symbols[effect].length)];
    el.style.fontSize = (effect === "Hail" ? rand(10, 20) : rand(13, 25)) + "px";
    el.style.opacity = rand(.45, .95);
    particles.appendChild(el);
    items.push({
      el,
      x: rand(0, 100),
      y: rand(-100, 110),
      vx: effect === "Wind gust" ? rand(1.2, 3.2) : effect === "Tornado" ? rand(-1.1, 1.1) : rand(-.25, .25),
      vy: effect === "Rain" ? rand(1.8, 3.8) : effect === "Hail" ? rand(1.4, 3.0) :
          effect === "Snow" ? rand(.35, 1.15) : effect === "Confetti" ? rand(.6, 1.7) :
          effect === "Tornado" ? rand(.7, 1.8) : rand(-.1, .2),
      phase: rand(0, Math.PI * 2),
      size: rand(.7, 1.4),
      spin: rand(-5, 5)
    });
  }
}

let last = performance.now();
function animate(now) {
  const dt = Math.min((now - last) / 16.67, 2.5);
  last = now;
  const w = stage.clientWidth, h = stage.clientHeight;
  for (const p of items) {
    if (effect === "Tornado") {
      const center = 50 + Math.sin(now / 850 + p.phase) * 13;
      p.x += (center - p.x) * .018 * dt + Math.sin(now / 170 + p.phase) * .32 * dt;
      p.y += p.vy * speedFactor * dt;
      p.el.style.transform = `translate(${p.x / 100 * w}px, ${p.y / 100 * h}px) rotate(${now / 3 + p.phase * 80}deg) scale(${p.size})`;
    } else if (effect === "Wind gust") {
      p.x += p.vx * speedFactor * dt;
      p.y += Math.sin(now / 180 + p.phase) * .25 * dt;
      p.el.style.transform = `translate(${p.x / 100 * w}px, ${p.y / 100 * h}px) rotate(${p.x * 2}deg)`;
    } else {
      p.x += p.vx * dt + (effect === "Snow" ? Math.sin(now / 400 + p.phase) * .18 * dt : 0);
      p.y += p.vy * speedFactor * dt;
      const rotate = effect === "Confetti" ? now / 9 + p.phase * 30 : effect === "Hail" ? 0 : now / 30 + p.phase * 15;
      p.el.style.transform = `translate(${p.x / 100 * w}px, ${p.y / 100 * h}px) rotate(${rotate}deg) scale(${p.size})`;
    }
    if (p.y > 112 || p.x > 112 || p.x < -12) {
      p.y = rand(-18, -3);
      p.x = effect === "Wind gust" ? rand(-12, -2) : rand(0, 100);
    }
  }
  requestAnimationFrame(animate);
}
requestAnimationFrame(animate);
</script>
</body>
</html>
""".replace("__CONFIG__", config_json)

components.html(html_doc, height=635, scrolling=False)

st.markdown(
    "Built with **Streamlit** and a browser-based animation preview. "
    "The motion runs inside the preview, so the whole Streamlit page does not need to refresh continuously."
)
