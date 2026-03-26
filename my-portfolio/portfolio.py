#!/usr/bin/env python3
from flask import Flask, render_template_string, send_from_directory
import os

app = Flask(__name__)
IMAGE_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), "images")

SLIDES = [
    {"type": "single", "file": "Kiosk.png"},
    {"type": "single", "file": "Communication_tool.png", "href": "/communication-tool"},
    {"type": "single", "file": "drone.png"},
    {"type": "single", "file": "Headphones.jpg"},
    {"type": "single", "file": "AI_project.png"},
    {
        "type": "pyramid",
        "files": [
            "Clip.png",
            "Memor.png",
            "bear_robot.jpeg",
        ]
    },
    {
        "type": "pyramid",
        "files": [
            "Bedframe.jpeg",
            "Plantholder.png",
            "Memory_robot.png",
        ]
    },
]

BASE_STYLE = """
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    min-height: 100vh;
    background: linear-gradient(135deg, #dde3ef 0%, #e8ecf5 60%, #d8e0ef 100%);
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    font-family: "Segoe UI", system-ui, sans-serif;
    padding: 40px 20px;
  }
  h1 { font-size: 2rem; font-weight: 700; color: #1a1a1a; margin-bottom: 6px; letter-spacing: -0.01em; }
  .subtitle { font-size: 0.9rem; color: #888; margin-bottom: 32px; }
"""

HOME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Lenn van den Berg</title>
  <style>
    """ + BASE_STYLE + """
    .card {
      background: #fff; border-radius: 20px;
      box-shadow: 0 8px 40px rgba(0,0,0,0.10);
      padding: 24px; width: 100%; max-width: 760px;
      display: flex; align-items: center; gap: 16px;
    }
    .carousel-inner { flex: 1; overflow: hidden; border-radius: 12px; }
    .carousel-track { display: flex; transition: transform 0.4s cubic-bezier(0.25,0.46,0.45,0.94); }
    .carousel-slide {
      min-width: 100%; height: 380px;
      background: #f9f9f9; border-radius: 12px;
      display: flex; align-items: center; justify-content: center;
      position: relative;
    }
    .carousel-slide img.single {
      max-width: 100%; max-height: 380px;
      object-fit: contain; border-radius: 20px;
    }
    .slide-link {
      position: absolute; inset: 0;
      display: flex; align-items: center; justify-content: center;
      border-radius: 12px; text-decoration: none;
      cursor: pointer;
    }
    .slide-link img {
      max-width: 100%; max-height: 380px;
      object-fit: contain; border-radius: 20px;
      transition: opacity 0.2s;
    }
    .slide-link:hover img { opacity: 0.85; }
    .slide-link .hover-label {
      position: absolute;
      bottom: 16px; left: 50%; transform: translateX(-50%);
      background: rgba(0,0,0,0.55);
      color: #fff; font-size: 0.8rem; font-weight: 600;
      padding: 6px 16px; border-radius: 100px;
      opacity: 0; transition: opacity 0.2s;
      white-space: nowrap;
    }
    .slide-link:hover .hover-label { opacity: 1; }
    .pyramid {
      display: flex; flex-direction: column;
      align-items: center; justify-content: center;
      gap: 10px; width: 100%; height: 100%; padding: 12px;
    }
    .pyramid-top    { display: flex; justify-content: center; }
    .pyramid-bottom { display: flex; justify-content: center; gap: 10px; }
    .pyramid img    { object-fit: contain; border-radius: 20px; background: #f0f0f0; }
    .pyramid-top img    { width: 220px; height: 160px; border-radius: 20px; }
    .pyramid-bottom img { width: 180px; height: 150px; border-radius: 20px; }
    .row-3 {
      display: flex; align-items: center;
      justify-content: center; gap: 10px;
      width: 100%; height: 100%; padding: 12px;
    }
    .row-3 img {
      flex: 1; max-width: 220px; height: 340px;
      object-fit: contain; border-radius: 20px;
      background: #f0f0f0;
    }
    .arrow {
      width: 40px; height: 40px; border-radius: 50%;
      border: 1px solid #ddd; background: #fff; color: #555;
      font-size: 1.1rem; cursor: pointer;
      display: flex; align-items: center; justify-content: center;
      flex-shrink: 0; box-shadow: 0 2px 8px rgba(0,0,0,0.08);
      transition: background 0.2s; user-select: none;
    }
    .arrow:hover { background: #f5f5f5; }
    .dots { display: flex; justify-content: center; gap: 7px; margin-top: 20px; }
    .dot {
      width: 9px; height: 9px; border-radius: 50%;
      background: #d0d4de; cursor: pointer;
      transition: background 0.2s, transform 0.2s;
    }
    .dot.active { background: #2a2a2a; transform: scale(1.15); }
  </style>
</head>
<body>
  <h1>Lenn van den Berg</h1>
  <p class="subtitle">Project Gallery</p>

  <div class="card">
    <button class="arrow" onclick="manualMove(-1)">&#8249;</button>
    <div class="carousel-inner">
      <div class="carousel-track" id="track">

        {% for slide in slides %}
        <div class="carousel-slide">

          {% if slide.type == "single" %}
            {% if slide.get('href') %}
              <a class="slide-link" href="{{ slide.href }}">
                <img src="/images/{{ slide.file }}" alt="Project image" loading="lazy"/>
                <span class="hover-label">View project →</span>
              </a>
            {% else %}
              <img class="single" src="/images/{{ slide.file }}" alt="Project image" loading="lazy"/>
            {% endif %}

          {% elif slide.type == "pyramid" %}
            <div class="pyramid">
              <div class="pyramid-top">
                <img src="/images/{{ slide.files[0] }}" alt="Image 1" loading="lazy"/>
              </div>
              <div class="pyramid-bottom">
                <img src="/images/{{ slide.files[1] }}" alt="Image 2" loading="lazy"/>
                <img src="/images/{{ slide.files[2] }}" alt="Image 3" loading="lazy"/>
              </div>
            </div>

          {% elif slide.type == "row" %}
            <div class="row-3">
              {% for f in slide.files %}
              <img src="/images/{{ f }}" alt="Project image" loading="lazy"/>
              {% endfor %}
            </div>
          {% endif %}

        </div>
        {% endfor %}

      </div>
    </div>
    <button class="arrow" onclick="manualMove(1)">&#8250;</button>
  </div>

  <div class="dots" id="dots">
    {% for slide in slides %}
    <div class="dot {% if loop.first %}active{% endif %}" onclick="goTo({{ loop.index0 }})"></div>
    {% endfor %}
  </div>

  <script>
    let current = 0;
    const total = {{ slides|length }};
    const track = document.getElementById("track");
    const dots  = document.querySelectorAll(".dot");

    function goTo(n) {
      current = (n + total) % total;
      track.style.transform = `translateX(-${current * 100}%)`;
      dots.forEach((d, i) => d.classList.toggle("active", i === current));
    }
    function move(dir) { goTo(current + dir); }
    function manualMove(dir) { move(dir); resetTimer(); }

    let timer = setInterval(() => move(1), 5000);
    function resetTimer() {
      clearInterval(timer);
      timer = setInterval(() => move(1), 5000);
    }

    document.addEventListener("keydown", e => {
      if (e.key === "ArrowLeft")  { move(-1); resetTimer(); }
      if (e.key === "ArrowRight") { move(1);  resetTimer(); }
    });

    let startX = 0;
    track.addEventListener("touchstart", e => startX = e.touches[0].clientX, { passive: true });
    track.addEventListener("touchend",   e => {
      const dx = e.changedTouches[0].clientX - startX;
      if (Math.abs(dx) > 40) { move(dx < 0 ? 1 : -1); resetTimer(); }
    });
  </script>
</body>
</html>
"""

COMM_TOOL_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Communication Tool</title>
  <style>
    """ + BASE_STYLE + """
    body { justify-content: flex-start; padding-top: 60px; }

    .project-card {
      width: 100%; max-width: 760px;
      border-radius: 20px; overflow: hidden;
      box-shadow: 0 8px 40px rgba(0,0,0,0.12);
    }

    /* Hero image with title overlay */
    .hero {
      position: relative; width: 100%; height: 380px;
    }
    .hero img {
      width: 100%; height: 100%; object-fit: cover; display: block;
    }
    .hero-overlay {
      position: absolute; inset: 0;
      background: linear-gradient(to top, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.15) 60%, transparent 100%);
      display: flex; align-items: flex-end; justify-content: center;
      padding-bottom: 32px;
    }
    .hero-overlay h2 {
      color: #fff; font-size: 2rem; font-weight: 800;
      letter-spacing: -0.01em; text-shadow: 0 2px 8px rgba(0,0,0,0.4);
    }

    /* Thumbnail below */
    .thumb-section {
      background: #fff; padding: 24px;
      display: flex; justify-content: center;
    }
    .thumb-section img {
      width: 100%; max-width: 500px; border-radius: 16px;
      object-fit: cover; box-shadow: 0 4px 16px rgba(0,0,0,0.10);
    }

    /* Back button */
    .back-wrap {
      margin-top: 32px; display: flex; justify-content: center;
    }
    .btn-back {
      padding: 14px 48px; border-radius: 100px;
      background: #1a1a2e; color: #fff;
      font-size: 0.95rem; font-weight: 600;
      text-decoration: none; border: none; cursor: pointer;
      box-shadow: 0 4px 16px rgba(0,0,0,0.15);
      transition: background 0.2s, transform 0.2s;
    }
    .btn-back:hover { background: #2a2a4a; transform: translateY(-2px); }
  </style>
</head>
<body>

  <div class="project-card">
    <div class="hero">
      <img src="/images/Communication_Tool.png" alt="Communication Tool"/>
      <div class="hero-overlay">
        <h2>Communication Tool</h2>
      </div>
    </div>
    <div class="thumb-section">
      <img src="/images/Communication_Tool2.jpg" alt="Components"/>
    </div>
  </div>

  <div class="back-wrap">
    <a href="/" class="btn-back">Back</a>
  </div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HOME_HTML, slides=SLIDES)

@app.route("/communication-tool")
def communication_tool():
    return render_template_string(COMM_TOOL_HTML)

@app.route("/images/<path:filename>")
def serve_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

if __name__ == "__main__":
    app.run()

