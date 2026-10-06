import os
import io
import base64
import urllib.request
import zipfile
from PIL import Image

WORKSPACE = "/home/riku/Documents/github"
ASSETS_DIR = os.path.join(WORKSPACE, "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

print("--- Fixing Typo and Coordinates in id-dashboard.svg ---")

# 1. Download & Base64 Encode Fonts
def fetch_b64(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
    with urllib.request.urlopen(req) as r:
        return base64.b64encode(r.read()).decode('utf-8')

print("Fetching Space Grotesk Bold WOFF2...")
space_grotesk_b64 = fetch_b64('https://fonts.gstatic.com/s/spacegrotesk/v22/V8mDoQDjQSkFtoMM3T6r8E7mPbF4C_k3HqU.woff2')

print("Fetching JetBrains Mono 600 WOFF2...")
jetbrains_mono_b64 = fetch_b64('https://fonts.gstatic.com/s/jetbrainsmono/v24/tDbY2o-flEEny0FZhsfKu5WU4zr3E_BX0PnT8RD8FqtTOlOVk6OThhvA.woff2')

FONT_FACE_CSS = f"""
/*
  Space Grotesk Font (OFL License - SIL Open Font License, Version 1.1)
  JetBrains Mono Font (OFL License - SIL Open Font License, Version 1.1)
*/
@font-face {{
  font-family: 'Space Grotesk';
  font-style: normal;
  font-weight: 700;
  src: url(data:font/woff2;base64,{space_grotesk_b64}) format('woff2');
}}
@font-face {{
  font-family: 'JetBrains Mono';
  font-style: normal;
  font-weight: 600;
  src: url(data:font/woff2;base64,{jetbrains_mono_b64}) format('woff2');
}}
"""

# 2. Process PNG images
print("Processing id.png...")
id_im = Image.open(os.path.join(WORKSPACE, 'id.png'))
id_im.thumbnail((700, 700), Image.Resampling.LANCZOS)
buf_id = io.BytesIO()
id_im.save(buf_id, format='PNG', optimize=True)
id_b64 = base64.b64encode(buf_id.getvalue()).decode('utf-8')

print("Processing right_pointing.png...")
right_im = Image.open(os.path.join(WORKSPACE, 'right_pointing.png'))
right_im.thumbnail((700, 700), Image.Resampling.LANCZOS)
buf_right = io.BytesIO()
right_im.save(buf_right, format='PNG', optimize=True)
right_b64 = base64.b64encode(buf_right.getvalue()).decode('utf-8')


# ==============================================================================
# SVG 1: hero.svg
# ==============================================================================
hero_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 360" width="100%" height="100%">
  <defs>
    <style>
      {FONT_FACE_CSS}
      
      .hero-title {{ font-family: 'Space Grotesk', system-ui, sans-serif; font-weight: 700; font-size: 38px; fill: url(#hero-name-grad); }}
      .hero-sub {{ font-family: 'JetBrains Mono', monospace; font-weight: 600; font-size: 14px; fill: #94a3b8; letter-spacing: 1px; }}
      .hero-role {{ font-family: 'Space Grotesk', system-ui, sans-serif; font-weight: 700; font-size: 20px; fill: #38bdf8; }}
      .hero-pitch {{ font-family: 'JetBrains Mono', monospace; font-size: 12.5px; fill: #cbd5e1; }}
      .hero-badge-text {{ font-family: 'JetBrains Mono', monospace; font-size: 11px; fill: #38bdf8; font-weight: 600; }}
      .hero-pill-text {{ font-family: 'JetBrains Mono', monospace; font-size: 11px; fill: #94a3b8; }}
      
      .anim-fade-1 {{ animation: heroFade 0.6s ease-out forwards; }}
      .anim-fade-2 {{ animation: heroFade 0.8s ease-out forwards; }}
      .anim-fade-3 {{ animation: heroFade 1.0s ease-out forwards; }}
      
      @keyframes heroFade {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
      }}

      .role-step1 {{ animation: roleCycle1 12s infinite; }}
      .role-step2 {{ animation: roleCycle2 12s infinite; }}
      .role-step3 {{ animation: roleCycle3 12s infinite; }}
      .role-step4 {{ animation: roleCycle4 12s infinite; }}
      
      @keyframes roleCycle1 {{
        0%, 22% {{ opacity: 1; }}
        25%, 97% {{ opacity: 0; }}
        100% {{ opacity: 1; }}
      }}
      @keyframes roleCycle2 {{
        0%, 22% {{ opacity: 0; }}
        25%, 47% {{ opacity: 1; }}
        50%, 100% {{ opacity: 0; }}
      }}
      @keyframes roleCycle3 {{
        0%, 47% {{ opacity: 0; }}
        50%, 72% {{ opacity: 1; }}
        75%, 100% {{ opacity: 0; }}
      }}
      @keyframes roleCycle4 {{
        0%, 72% {{ opacity: 0; }}
        75%, 97% {{ opacity: 1; }}
        100% {{ opacity: 0; }}
      }}

      .pulse-dot {{ animation: pulseGlow 2s infinite alternate; }}
      @keyframes pulseGlow {{
        0% {{ opacity: 0.6; }}
        100% {{ opacity: 1; }}
      }}

      @media (prefers-reduced-motion: reduce) {{
        .anim-fade-1, .anim-fade-2, .anim-fade-3, .role-step1, .role-step2, .role-step3, .role-step4, .pulse-dot {{
          animation: none !important;
          opacity: 1 !important;
        }}
        .role-step2, .role-step3, .role-step4 {{ display: none; }}
      }}
    </style>

    <linearGradient id="hero-bg-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#070b16"/>
      <stop offset="50%" stop-color="#0d1527"/>
      <stop offset="100%" stop-color="#070b16"/>
    </linearGradient>

    <linearGradient id="hero-name-grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="40%" stop-color="#60a5fa"/>
      <stop offset="80%" stop-color="#247bff"/>
      <stop offset="100%" stop-color="#ff354f"/>
    </linearGradient>

    <linearGradient id="hero-border-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.6"/>
      <stop offset="50%" stop-color="#1e293b" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#ff354f" stop-opacity="0.6"/>
    </linearGradient>

    <radialGradient id="hero-glow-blue" cx="0.8" cy="0.3" r="0.6">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#247bff" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="hero-glow-red" cx="0.2" cy="0.8" r="0.6">
      <stop offset="0%" stop-color="#ff354f" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#ff354f" stop-opacity="0"/>
    </radialGradient>

    <pattern id="hero-dots" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1" fill="#334155" opacity="0.3"/>
    </pattern>
  </defs>

  <rect width="850" height="360" rx="16" fill="url(#hero-bg-grad)"/>
  <rect width="850" height="360" rx="16" fill="url(#hero-dots)"/>
  <rect width="850" height="360" rx="16" fill="url(#hero-glow-blue)"/>
  <rect width="850" height="360" rx="16" fill="url(#hero-glow-red)"/>
  <rect x="0.5" y="0.5" width="849" height="359" rx="15.5" fill="none" stroke="url(#hero-border-grad)" stroke-width="1"/>

  <g class="anim-fade-1">
    <rect x="40" y="32" width="310" height="26" rx="13" fill="#0f172a" stroke="#1e293b" stroke-width="1"/>
    <circle cx="56" cy="45" r="4" fill="#10b981" class="pulse-dot"/>
    <text x="68" y="49" class="hero-badge-text">AVAILABLE FOR BACKEND &amp; AI/ML ROLES</text>
  </g>

  <text x="40" y="92" class="hero-sub anim-fade-1">WELCOME | I'M</text>
  <text x="40" y="136" class="hero-title anim-fade-2">MANABENDU KARFA</text>

  <g class="anim-fade-2">
    <text x="40" y="172" class="hero-role role-step1">Java Backend Developer</text>
    <text x="40" y="172" class="hero-role role-step2">Software Developer</text>
    <text x="40" y="172" class="hero-role role-step3">AI/ML &amp; RAG Engineer</text>
    <text x="40" y="172" class="hero-role role-step4">Full Stack Developer</text>
  </g>

  <g class="anim-fade-3">
    <text x="40" y="212" class="hero-pitch">B.E. AI/ML student &amp; Software Developer focused on building</text>
    <text x="40" y="230" class="hero-pitch">scalable Java/Spring Boot backends, event-driven microservices,</text>
    <text x="40" y="248" class="hero-pitch">and production-grade AI-powered applications.</text>
  </g>

  <g class="anim-fade-3">
    <rect x="40" y="288" width="460" height="34" rx="8" fill="#0d1424" stroke="#1e293b" stroke-width="1"/>
    <text x="54" y="309" class="hero-pill-text">Bangalore, India  |  CiTech (CGPA 8.31)  |  TwinTallies Intern</text>
  </g>

  <g transform="translate(520, 15)" class="anim-fade-1">
    <circle cx="150" cy="165" r="130" fill="#247bff" opacity="0.12"/>
    <circle cx="150" cy="165" r="100" fill="#ff354f" opacity="0.1"/>
    <circle cx="150" cy="165" r="145" fill="none" stroke="#247bff" stroke-width="1" stroke-dasharray="6 8" opacity="0.4"/>
    <circle cx="150" cy="165" r="152" fill="none" stroke="#ff354f" stroke-width="1" stroke-dasharray="3 12" opacity="0.3"/>
    <image href="data:image/png;base64,{id_b64}" x="0" y="5" width="300" height="320" preserveAspectRatio="xMidYMid meet"/>
  </g>
</svg>"""

with open(os.path.join(ASSETS_DIR, "hero.svg"), "w", encoding="utf-8") as f:
    f.write(hero_svg)

# ==============================================================================
# SVG 2: about-life.svg
# ==============================================================================
about_life_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 340" width="100%" height="100%">
  <defs>
    <style>
      {FONT_FACE_CSS}

      .card-header {{ font-family: 'Space Grotesk', system-ui, sans-serif; font-weight: 700; font-size: 15px; fill: #f8fafc; letter-spacing: 0.5px; }}
      .cap-title {{ font-family: 'Space Grotesk', system-ui, sans-serif; font-weight: 700; font-size: 13.5px; fill: #60a5fa; }}
      .cap-desc {{ font-family: 'JetBrains Mono', monospace; font-size: 11px; fill: #94a3b8; line-height: 1.4; }}
      
      .slide-title {{ font-family: 'Space Grotesk', system-ui, sans-serif; font-weight: 700; font-size: 18px; fill: #ffffff; letter-spacing: 0.5px; }}
      .slide-sub {{ font-family: 'Space Grotesk', system-ui, sans-serif; font-weight: 700; font-size: 13px; fill: #ff354f; }}
      .slide-desc {{ font-family: 'JetBrains Mono', monospace; font-size: 12px; fill: #cbd5e1; }}
      
      .bar-label {{ font-family: 'JetBrains Mono', monospace; font-size: 10px; fill: #64748b; font-weight: 600; }}

      .slide-1 {{ animation: slideAnim1 12s infinite; }}
      .slide-2 {{ animation: slideAnim2 12s infinite; }}
      .slide-3 {{ animation: slideAnim3 12s infinite; }}

      @keyframes slideAnim1 {{
        0%, 31% {{ opacity: 1; }}
        33%, 98% {{ opacity: 0; }}
        100% {{ opacity: 1; }}
      }}
      @keyframes slideAnim2 {{
        0%, 31% {{ opacity: 0; }}
        33%, 64% {{ opacity: 1; }}
        66%, 100% {{ opacity: 0; }}
      }}
      @keyframes slideAnim3 {{
        0%, 64% {{ opacity: 0; }}
        66%, 98% {{ opacity: 1; }}
        100% {{ opacity: 0; }}
      }}

      .pbar-fill-1 {{ animation: pfill1 12s linear infinite; }}
      .pbar-fill-2 {{ animation: pfill2 12s linear infinite; }}
      .pbar-fill-3 {{ animation: pfill3 12s linear infinite; }}

      @keyframes pfill1 {{
        0% {{ width: 0px; }}
        31% {{ width: 110px; }}
        33%, 100% {{ width: 0px; }}
      }}
      @keyframes pfill2 {{
        0%, 33% {{ width: 0px; }}
        64% {{ width: 110px; }}
        66%, 100% {{ width: 0px; }}
      }}
      @keyframes pfill3 {{
        0%, 66% {{ width: 0px; }}
        98% {{ width: 110px; }}
        100% {{ width: 0px; }}
      }}

      @media (prefers-reduced-motion: reduce) {{
        .slide-1, .slide-2, .slide-3, .pbar-fill-1, .pbar-fill-2, .pbar-fill-3 {{
          animation: none !important;
          opacity: 1 !important;
        }}
        .slide-2, .slide-3 {{ display: none; }}
        .pbar-fill-1 {{ width: 110px !important; }}
      }}
    </style>

    <linearGradient id="life-bg-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#070b16"/>
      <stop offset="100%" stop-color="#0d1428"/>
    </linearGradient>

    <linearGradient id="life-card-border" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#ff354f" stop-opacity="0.4"/>
    </linearGradient>

    <linearGradient id="bar-fill-grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#247bff"/>
      <stop offset="100%" stop-color="#ff354f"/>
    </linearGradient>
  </defs>

  <rect width="850" height="340" rx="16" fill="url(#life-bg-grad)"/>
  <rect x="0.5" y="0.5" width="849" height="339" rx="15.5" fill="none" stroke="url(#life-card-border)" stroke-width="1"/>

  <g>
    <rect x="24" y="24" width="380" height="292" rx="12" fill="#0b1120" stroke="#1e293b" stroke-width="1"/>
    <path d="M 44 44 L 44 58 M 44 51 L 56 51" stroke="#247bff" stroke-width="3" stroke-linecap="round"/>
    <text x="62" y="56" class="card-header">CORE CAPABILITIES</text>

    <rect x="48" y="82" width="12" height="12" rx="3" fill="#247bff"/>
    <text x="72" y="92" class="cap-title">Backend &amp; Microservices</text>
    <text x="72" y="107" class="cap-desc">Spring Boot, Spring Cloud, Kafka event pipelines,</text>
    <text x="72" y="120" class="cap-desc">Keycloak OAuth2/JWT security &amp; API Gateways.</text>

    <rect x="48" y="140" width="12" height="12" rx="3" fill="#60a5fa"/>
    <text x="72" y="150" class="cap-title">AI &amp; RAG Document Intelligence</text>
    <text x="72" y="165" class="cap-desc">Docling PDF parsing, FAISS vector embeddings,</text>
    <text x="72" y="178" class="cap-desc">Llama 3.3 70B &amp; LangChain automated pipelines.</text>

    <rect x="48" y="198" width="12" height="12" rx="3" fill="#38bdf8"/>
    <text x="72" y="208" class="cap-title">Cloud &amp; Observability</text>
    <text x="72" y="223" class="cap-desc">Micrometer metrics, Prometheus, Grafana,</text>
    <text x="72" y="236" class="cap-desc">InfluxDB time-series telemetry &amp; Docker Compose.</text>

    <rect x="48" y="256" width="12" height="12" rx="3" fill="#ff354f"/>
    <text x="72" y="266" class="cap-title">Full-Stack &amp; Scalable APIs</text>
    <text x="72" y="281" class="cap-desc">FastAPI backends, RESTful microservices,</text>
    <text x="72" y="294" class="cap-desc">React frontends, PostgreSQL, MySQL &amp; Redis.</text>
  </g>

  <g>
    <rect x="424" y="24" width="402" height="292" rx="12" fill="#0b1120" stroke="#1e293b" stroke-width="1"/>
    <text x="448" y="56" class="card-header">BEYOND THE CODE</text>
    <rect x="754" y="42" width="50" height="20" rx="10" fill="#1e293b"/>
    <text x="766" y="56" class="bar-label">LIFE</text>

    <g class="slide-1">
      <rect x="448" y="88" width="354" height="150" rx="10" fill="#0f172a" stroke="#1e293b" stroke-width="1"/>
      <text x="468" y="122" class="slide-title">CYCLING</text>
      <text x="468" y="140" class="slide-sub">Endurance &amp; Outdoor Energy</text>
      <text x="468" y="173" class="slide-desc">Avid cyclist exploring long routes across Bangalore.</text>
      <text x="468" y="193" class="slide-desc">Building physical resilience, discipline, and focus that</text>
      <text x="468" y="213" class="slide-desc">translates directly into high-intensity engineering.</text>
    </g>

    <g class="slide-2">
      <rect x="448" y="88" width="354" height="150" rx="10" fill="#0f172a" stroke="#1e293b" stroke-width="1"/>
      <text x="468" y="122" class="slide-title">MUSIC &amp; SINGING</text>
      <text x="468" y="140" class="slide-sub">Rhythm &amp; Harmony</text>
      <text x="468" y="173" class="slide-desc">Passionate about vocal music and acoustic tracks.</text>
      <text x="468" y="193" class="slide-desc">Finding harmony, creative rhythm, and deep work focus</text>
      <text x="468" y="213" class="slide-desc">through melodies during complex coding sessions.</text>
    </g>

    <g class="slide-3">
      <rect x="448" y="88" width="354" height="150" rx="10" fill="#0f172a" stroke="#1e293b" stroke-width="1"/>
      <text x="468" y="122" class="slide-title">HACKATHONS &amp; LEADERSHIP</text>
      <text x="468" y="140" class="slide-sub">2nd Place @ HACKTRONICS &amp; Maths Club</text>
      <text x="468" y="173" class="slide-desc">Secured 2nd Place in Agritech @ HACKTRONICS (CMRIT).</text>
      <text x="468" y="193" class="slide-desc">Served as Maths Club President @ St. Joseph's PUC,</text>
      <text x="468" y="213" class="slide-desc">organizing events and leading technical teams.</text>
    </g>

    <text x="448" y="270" class="bar-label">01 CYCLING</text>
    <rect x="448" y="276" width="110" height="6" rx="3" fill="#1e293b"/>
    <rect x="448" y="276" width="0" height="6" rx="3" fill="url(#bar-fill-grad)" class="pbar-fill-1"/>

    <text x="570" y="270" class="bar-label">02 MUSIC</text>
    <rect x="570" y="276" width="110" height="6" rx="3" fill="#1e293b"/>
    <rect x="570" y="276" width="0" height="6" rx="3" fill="url(#bar-fill-grad)" class="pbar-fill-2"/>

    <text x="692" y="270" class="bar-label">03 HACKATHONS</text>
    <rect x="692" y="276" width="110" height="6" rx="3" fill="#1e293b"/>
    <rect x="692" y="276" width="0" height="6" rx="3" fill="url(#bar-fill-grad)" class="pbar-fill-3"/>
  </g>
</svg>"""

with open(os.path.join(ASSETS_DIR, "about-life.svg"), "w", encoding="utf-8") as f:
    f.write(about_life_svg)

# ==============================================================================
# SVG 3: stack.svg
# ==============================================================================
stack_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 360" width="100%" height="100%">
  <defs>
    <style>
      {FONT_FACE_CSS}

      .stack-title {{ font-family: 'Space Grotesk', system-ui, sans-serif; font-weight: 700; font-size: 16px; fill: #ffffff; letter-spacing: 0.5px; }}
      .orbit-node-text {{ font-family: 'JetBrains Mono', monospace; font-size: 10.5px; fill: #cbd5e1; font-weight: 600; }}
      .cat-title {{ font-family: 'Space Grotesk', system-ui, sans-serif; font-weight: 700; font-size: 13px; fill: #60a5fa; letter-spacing: 0.3px; }}
      .chip-text {{ font-family: 'JetBrains Mono', monospace; font-size: 11px; fill: #e2e8f0; font-weight: 600; }}
    </style>

    <linearGradient id="stack-bg-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#070b16"/>
      <stop offset="50%" stop-color="#0b1326"/>
      <stop offset="100%" stop-color="#070b16"/>
    </linearGradient>

    <linearGradient id="stack-border-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#ff354f" stop-opacity="0.5"/>
    </linearGradient>

    <linearGradient id="orbit-grad-1" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.7"/>
      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.2"/>
    </linearGradient>

    <linearGradient id="orbit-grad-2" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ff354f" stop-opacity="0.7"/>
      <stop offset="100%" stop-color="#a855f7" stop-opacity="0.2"/>
    </linearGradient>
  </defs>

  <rect width="850" height="360" rx="16" fill="url(#stack-bg-grad)"/>
  <rect x="0.5" y="0.5" width="849" height="359" rx="15.5" fill="none" stroke="url(#stack-border-grad)" stroke-width="1"/>

  <circle cx="425" cy="90" r="34" fill="#0f172a" stroke="#247bff" stroke-width="2"/>
  <circle cx="425" cy="90" r="42" fill="none" stroke="#247bff" stroke-width="1" stroke-dasharray="4 4" opacity="0.5"/>
  <text x="425" y="86" font-family="'Space Grotesk', sans-serif" font-weight="700" font-size="12" fill="#ffffff" text-anchor="middle">TECH</text>
  <text x="425" y="100" font-family="'Space Grotesk', sans-serif" font-weight="700" font-size="12" fill="#60a5fa" text-anchor="middle">MATRIX</text>

  <ellipse cx="425" cy="90" rx="340" ry="55" fill="none" stroke="url(#orbit-grad-1)" stroke-width="1.5" stroke-dasharray="6 6" transform="rotate(-5, 425, 90)"/>
  
  <g>
    <rect x="110" y="53" width="70" height="24" rx="12" fill="#0f172a" stroke="#247bff" stroke-width="1"/>
    <text x="145" y="69" class="orbit-node-text" text-anchor="middle">Java</text>

    <rect x="243" y="126" width="94" height="24" rx="12" fill="#0f172a" stroke="#10b981" stroke-width="1"/>
    <text x="290" y="142" class="orbit-node-text" text-anchor="middle">Spring Boot</text>

    <rect x="525" y="33" width="70" height="24" rx="12" fill="#0f172a" stroke="#a855f7" stroke-width="1"/>
    <text x="560" y="49" class="orbit-node-text" text-anchor="middle">Kafka</text>

    <rect x="673" y="98" width="84" height="24" rx="12" fill="#0f172a" stroke="#ff354f" stroke-width="1"/>
    <text x="715" y="114" class="orbit-node-text" text-anchor="middle">RAG / LLM</text>
  </g>

  <ellipse cx="425" cy="90" rx="220" ry="38" fill="none" stroke="url(#orbit-grad-2)" stroke-width="1.5" transform="rotate(4, 425, 90)"/>
  
  <g>
    <rect x="207" y="98" width="76" height="24" rx="12" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>
    <text x="245" y="114" class="orbit-node-text" text-anchor="middle">Python</text>

    <rect x="383" y="40" width="84" height="24" rx="12" fill="#0f172a" stroke="#06b6d4" stroke-width="1"/>
    <text x="425" y="56" class="orbit-node-text" text-anchor="middle">FastAPI</text>

    <rect x="553" y="100" width="84" height="24" rx="12" fill="#0f172a" stroke="#247bff" stroke-width="1"/>
    <text x="595" y="116" class="orbit-node-text" text-anchor="middle">Docker</text>
  </g>

  <line x1="40" y1="168" x2="810" y2="168" stroke="#1e293b" stroke-width="1" stroke-dasharray="4 4"/>

  <text x="40" y="198" class="cat-title">LANGUAGES</text>
  <rect x="40" y="208" width="72" height="26" rx="6" fill="#0d1527" stroke="#1e293b" stroke-width="1"/>
  <text x="50" y="225" class="chip-text">Java</text>
  
  <rect x="118" y="208" width="80" height="26" rx="6" fill="#0d1527" stroke="#1e293b" stroke-width="1"/>
  <text x="128" y="225" class="chip-text">Python</text>
  
  <rect x="204" y="208" width="50" height="26" rx="6" fill="#0d1527" stroke="#1e293b" stroke-width="1"/>
  <text x="214" y="225" class="chip-text">C</text>
  
  <rect x="260" y="208" width="102" height="26" rx="6" fill="#0d1527" stroke="#1e293b" stroke-width="1"/>
  <text x="270" y="225" class="chip-text">JavaScript</text>

  <text x="440" y="198" class="cat-title">BACKEND &amp; MICROSERVICES</text>
  <rect x="440" y="208" width="94" height="26" rx="6" fill="#0d1527" stroke="#1e293b" stroke-width="1"/>
  <text x="450" y="225" class="chip-text">Spring Boot</text>
  
  <rect x="540" y="208" width="118" height="26" rx="6" fill="#0d1527" stroke="#1e293b" stroke-width="1"/>
  <text x="550" y="225" class="chip-text">Spring Security</text>
  
  <rect x="664" y="208" width="78" height="26" rx="6" fill="#0d1527" stroke="#1e293b" stroke-width="1"/>
  <text x="674" y="225" class="chip-text">FastAPI</text>
  
  <rect x="748" y="208" width="62" height="26" rx="6" fill="#0d1527" stroke="#1e293b" stroke-width="1"/>
  <text x="758" y="225" class="chip-text">Kafka</text>

  <text x="40" y="278" class="cat-title">AI / ML &amp; RAG ARCHITECTURE</text>
  <rect x="40" y="288" width="82" height="26" rx="6" fill="#0d1527" stroke="#1e293b" stroke-width="1"/>
  <text x="50" y="305" class="chip-text">Spring AI</text>

  <rect x="128" y="288" width="92" height="26" rx="6" fill="#0d1527" stroke="#1e293b" stroke-width="1"/>
  <text x="138" y="305" class="chip-text">LangChain</text>

  <rect x="226" y="288" width="90" height="26" rx="6" fill="#0d1527" stroke="#1e293b" stroke-width="1"/>
  <text x="236" y="305" class="chip-text">LangGraph</text>

  <rect x="322" y="288" width="88" height="26" rx="6" fill="#0d1527" stroke="#1e293b" stroke-width="1"/>
  <text x="332" y="305" class="chip-text">Docling RAG</text>

  <text x="440" y="278" class="cat-title">DATABASES &amp; CLOUD DEVOPS</text>
  <rect x="440" y="288" width="68" height="26" rx="6" fill="#0d1527" stroke="#1e293b" stroke-width="1"/>
  <text x="450" y="305" class="chip-text">MySQL</text>

  <rect x="514" y="288" width="92" height="26" rx="6" fill="#0d1527" stroke="#1e293b" stroke-width="1"/>
  <text x="524" y="305" class="chip-text">PostgreSQL</text>

  <rect x="612" y="288" width="80" height="26" rx="6" fill="#0d1527" stroke="#1e293b" stroke-width="1"/>
  <text x="622" y="305" class="chip-text">MongoDB</text>

  <rect x="698" y="288" width="62" height="26" rx="6" fill="#0d1527" stroke="#1e293b" stroke-width="1"/>
  <text x="708" y="305" class="chip-text">Redis</text>

  <rect x="766" y="288" width="68" height="26" rx="6" fill="#0d1527" stroke="#1e293b" stroke-width="1"/>
  <text x="776" y="305" class="chip-text">Docker</text>
</svg>"""

with open(os.path.join(ASSETS_DIR, "stack.svg"), "w", encoding="utf-8") as f:
    f.write(stack_svg)

# ==============================================================================
# SVG 4: id-dashboard.svg (FIXED ROW 2 TYPO y=208 + OPTIMIZED CARD TEXT)
# ==============================================================================
id_dashboard_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 400" width="100%" height="100%">
  <defs>
    <style>
      {FONT_FACE_CSS}

      .id-card-title {{ font-family: 'Space Grotesk', system-ui, sans-serif; font-weight: 700; font-size: 15px; fill: #ffffff; letter-spacing: 0.5px; }}
      .id-card-sub {{ font-family: 'JetBrains Mono', monospace; font-size: 10px; fill: #60a5fa; font-weight: 600; }}
      .id-card-role {{ font-family: 'JetBrains Mono', monospace; font-size: 9.5px; fill: #94a3b8; }}
      .id-code {{ font-family: 'JetBrains Mono', monospace; font-size: 9px; fill: #64748b; letter-spacing: 2px; }}

      .dash-title {{ font-family: 'Space Grotesk', system-ui, sans-serif; font-weight: 700; font-size: 16px; fill: #ffffff; letter-spacing: 0.5px; }}
      .metric-val {{ font-family: 'Space Grotesk', system-ui, sans-serif; font-weight: 700; font-size: 22px; fill: #60a5fa; }}
      .metric-lbl {{ font-family: 'Space Grotesk', system-ui, sans-serif; font-weight: 700; font-size: 12.5px; fill: #f8fafc; }}
      .metric-desc {{ font-family: 'JetBrains Mono', monospace; font-size: 10.5px; fill: #94a3b8; line-height: 1.4; }}

      .foil-sweep {{ animation: foilAnim 6s linear infinite; }}
      @keyframes foilAnim {{
        0% {{ transform: translateX(-220px) skewX(-25deg); }}
        30%, 100% {{ transform: translateX(280px) skewX(-25deg); }}
      }}

      @media (prefers-reduced-motion: reduce) {{
        .foil-sweep {{ animation: none !important; }}
      }}
    </style>

    <linearGradient id="dash-bg-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#070b16"/>
      <stop offset="50%" stop-color="#0c1429"/>
      <stop offset="100%" stop-color="#070b16"/>
    </linearGradient>

    <linearGradient id="dash-border-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#ff354f" stop-opacity="0.5"/>
    </linearGradient>

    <linearGradient id="id-card-bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#090d16"/>
    </linearGradient>

    <linearGradient id="lanyard-grad-left" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#247bff"/>
      <stop offset="100%" stop-color="#1d4ed8"/>
    </linearGradient>

    <linearGradient id="lanyard-grad-right" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ff354f"/>
      <stop offset="100%" stop-color="#be123c"/>
    </linearGradient>

    <linearGradient id="foil-grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="50%" stop-color="#ffffff" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>

    <clipPath id="id-card-clip">
      <rect x="30" y="55" width="210" height="325" rx="16"/>
    </clipPath>
  </defs>

  <rect width="850" height="400" rx="16" fill="url(#dash-bg-grad)"/>
  <rect x="0.5" y="0.5" width="849" height="399" rx="15.5" fill="none" stroke="url(#dash-border-grad)" stroke-width="1"/>

  <!-- Left Side: Hanging Lanyard ID Card -->
  <g>
    <animateTransform attributeName="transform" type="rotate" values="-6 135 25; 4 135 25; -2 135 25; 1.7 135 25; -1.7 135 25; 1.7 135 25" keyTimes="0; 0.15; 0.3; 0.45; 0.7; 1" dur="12s" repeatCount="indefinite"/>

    <path d="M 115 0 L 130 45" stroke="url(#lanyard-grad-left)" stroke-width="6" stroke-linecap="round"/>
    <path d="M 155 0 L 140 45" stroke="url(#lanyard-grad-right)" stroke-width="6" stroke-linecap="round"/>

    <rect x="125" y="40" width="20" height="14" rx="3" fill="#64748b" stroke="#cbd5e1" stroke-width="1"/>
    <circle cx="135" cy="47" r="3" fill="#0f172a"/>
    <rect x="120" y="52" width="30" height="6" rx="2" fill="#94a3b8"/>

    <g clip-path="url(#id-card-clip)">
      <rect x="30" y="55" width="210" height="325" rx="16" fill="url(#id-card-bg)" stroke="#1e293b" stroke-width="1.5"/>

      <rect x="30" y="55" width="210" height="28" fill="#1e293b"/>
      <circle cx="135" cy="67" r="4" fill="#0f172a"/>
      
      <text x="135" y="96" class="id-card-sub" text-anchor="middle">CAMBRIDGE INST. OF TECH</text>

      <rect x="65" y="106" width="140" height="135" rx="10" fill="#0b1120" stroke="#247bff" stroke-width="1"/>
      <image href="data:image/png;base64,{id_b64}" x="55" y="96" width="160" height="155" preserveAspectRatio="xMidYMid meet"/>

      <text x="135" y="260" class="id-card-title" text-anchor="middle">MANABENDU KARFA</text>
      <text x="135" y="276" class="id-card-role" text-anchor="middle">B.E. AI/ML Student | Dev Intern</text>
      <text x="135" y="290" class="id-card-role" text-anchor="middle">TwinTallies Private Limited</text>

      <g>
        <rect x="55" y="304" width="2" height="20" fill="#cbd5e1"/>
        <rect x="59" y="304" width="4" height="20" fill="#cbd5e1"/>
        <rect x="65" y="304" width="1" height="20" fill="#cbd5e1"/>
        <rect x="68" y="304" width="3" height="20" fill="#cbd5e1"/>
        <rect x="73" y="304" width="2" height="20" fill="#cbd5e1"/>
        <rect x="77" y="304" width="5" height="20" fill="#cbd5e1"/>
        <rect x="84" y="304" width="1" height="20" fill="#cbd5e1"/>
        <rect x="87" y="304" width="3" height="20" fill="#cbd5e1"/>
        <rect x="92" y="304" width="2" height="20" fill="#cbd5e1"/>
        <rect x="96" y="304" width="4" height="20" fill="#cbd5e1"/>
        <rect x="102" y="304" width="1" height="20" fill="#cbd5e1"/>
        <rect x="105" y="304" width="6" height="20" fill="#cbd5e1"/>
        <rect x="113" y="304" width="2" height="20" fill="#cbd5e1"/>
        <rect x="117" y="304" width="3" height="20" fill="#cbd5e1"/>
        <rect x="122" y="304" width="1" height="20" fill="#cbd5e1"/>
        <rect x="125" y="304" width="5" height="20" fill="#cbd5e1"/>
        <rect x="132" y="304" width="2" height="20" fill="#cbd5e1"/>
        <rect x="136" y="304" width="4" height="20" fill="#cbd5e1"/>
        <rect x="142" y="304" width="1" height="20" fill="#cbd5e1"/>
        <rect x="145" y="304" width="3" height="20" fill="#cbd5e1"/>
        <rect x="150" y="304" width="5" height="20" fill="#cbd5e1"/>
        <rect x="157" y="304" width="2" height="20" fill="#cbd5e1"/>
        <rect x="161" y="304" width="4" height="20" fill="#cbd5e1"/>
        <text x="135" y="338" class="id-code" text-anchor="middle">ID: 890BA52A3</text>
      </g>

      <rect x="0" y="55" width="60" height="325" fill="url(#foil-grad)" class="foil-sweep"/>
    </g>
  </g>

  <!-- Right Side: Verified Dashboard Metrics (x: 270 to 824) -->
  <g>
    <text x="270" y="48" class="dash-title">VERIFIED MILESTONES &amp; ACADEMICS</text>

    <!-- Card 1: CGPA (Row 1 Left: x=270, y=68) -->
    <rect x="270" y="68" width="268" height="92" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1"/>
    <text x="288" y="104" class="metric-val">8.31 CGPA</text>
    <text x="288" y="126" class="metric-lbl">B.E. AI &amp; Machine Learning</text>
    <text x="288" y="143" class="metric-desc">Cambridge Inst. of Tech (2024–2028)</text>

    <!-- Card 2: 12th Grade (Row 1 Right: x=554, y=68) -->
    <rect x="554" y="68" width="268" height="92" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1"/>
    <text x="572" y="104" class="metric-val" fill="#ff354f">96% Grade</text>
    <text x="572" y="126" class="metric-lbl">12th Standard (PCME)</text>
    <text x="572" y="143" class="metric-desc">St. Joseph's Pre-University College (2024)</text>

    <!-- Card 3: Hacktronics 2nd Place (Row 2 Left: x=270, y=172) -> FIXED y=208! -->
    <rect x="270" y="172" width="268" height="92" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1"/>
    <text x="288" y="208" class="metric-val" fill="#f59e0b">2nd Place</text>
    <text x="288" y="230" class="metric-lbl">Agritech @ HACKTRONICS</text>
    <text x="288" y="247" class="metric-desc">CMRIT Circuit to Cloud Hackathon</text>

    <!-- Card 4: Software Dev Internship (Row 2 Right: x=554, y=172) -->
    <rect x="554" y="172" width="268" height="92" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1"/>
    <text x="572" y="208" class="metric-val" fill="#10b981">TwinTallies</text>
    <text x="572" y="230" class="metric-lbl">Software Developer Intern</text>
    <text x="572" y="247" class="metric-desc">Financial automation &amp; Java backends (2026)</text>

    <!-- Card 5: Rikify Microservices (Row 3 Left: x=270, y=276) -->
    <rect x="270" y="276" width="268" height="92" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1"/>
    <text x="288" y="312" class="metric-val">6 Microservices</text>
    <text x="288" y="334" class="metric-lbl">Rikify Energy Tracker</text>
    <text x="288" y="351" class="metric-desc">Spring Cloud, Kafka, InfluxDB &amp; Grafana</text>

    <!-- Card 6: YellowDoc.ai RAG (Row 3 Right: x=554, y=276) -->
    <rect x="554" y="276" width="268" height="92" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1"/>
    <text x="572" y="312" class="metric-val" fill="#a855f7">RAG &amp; Doc AI</text>
    <text x="572" y="334" class="metric-lbl">YellowDoc.ai Intelligence</text>
    <text x="572" y="351" class="metric-desc">Docling PDF, FAISS &amp; Llama 3.3 70B</text>
  </g>
</svg>"""

with open(os.path.join(ASSETS_DIR, "id-dashboard.svg"), "w", encoding="utf-8") as f:
    f.write(id_dashboard_svg)
print("Saved assets/id-dashboard.svg")

# ==============================================================================
# SVG 5: connect.svg
# ==============================================================================
connect_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 320" width="100%" height="100%">
  <defs>
    <style>
      {FONT_FACE_CSS}

      .conn-title {{ font-family: 'Space Grotesk', system-ui, sans-serif; font-weight: 700; font-size: 20px; fill: #ffffff; letter-spacing: 0.5px; }}
      .conn-sub {{ font-family: 'JetBrains Mono', monospace; font-size: 12px; fill: #94a3b8; }}

      .card-name {{ font-family: 'Space Grotesk', system-ui, sans-serif; font-weight: 700; font-size: 13.5px; fill: #f8fafc; }}
      .card-handle {{ font-family: 'JetBrains Mono', monospace; font-size: 10.5px; fill: #60a5fa; }}
      .arrow-icon {{ font-family: 'Space Grotesk', system-ui, sans-serif; font-weight: 700; font-size: 16px; fill: #247bff; }}
    </style>

    <linearGradient id="conn-bg-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#070b16"/>
      <stop offset="50%" stop-color="#0c1429"/>
      <stop offset="100%" stop-color="#070b16"/>
    </linearGradient>

    <linearGradient id="conn-border-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#ff354f" stop-opacity="0.5"/>
    </linearGradient>

    <radialGradient id="conn-blue-glow" cx="0.9" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#247bff" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <rect width="850" height="320" rx="16" fill="url(#conn-bg-grad)"/>
  <rect width="850" height="320" rx="16" fill="url(#conn-blue-glow)"/>
  <rect x="0.5" y="0.5" width="849" height="319" rx="15.5" fill="none" stroke="url(#conn-border-grad)" stroke-width="1"/>

  <image href="data:image/png;base64,{right_b64}" x="10" y="10" width="370" height="300" preserveAspectRatio="xMidYMid meet"/>

  <text x="390" y="48" class="conn-title">LET'S CONNECT &amp; BUILD</text>
  <text x="390" y="68" class="conn-sub">Open for Backend, AI/ML &amp; Full Stack roles</text>

  <rect x="390" y="88" width="210" height="84" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1"/>
  <rect x="406" y="118" width="24" height="24" rx="5" fill="#0077b5" opacity="0.2"/>
  <text x="412" y="135" font-family="'Space Grotesk', sans-serif" font-weight="700" font-size="15" fill="#0a66c2">in</text>
  <text x="444" y="126" class="card-name">LinkedIn</text>
  <text x="444" y="143" class="card-handle">manabendu-karfa</text>
  <text x="570" y="135" class="arrow-icon">➔</text>

  <rect x="614" y="88" width="210" height="84" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1"/>
  <rect x="630" y="118" width="24" height="24" rx="5" fill="#333333" opacity="0.4"/>
  <text x="634" y="135" font-family="'JetBrains Mono', monospace" font-weight="700" font-size="13" fill="#cbd5e1">&lt;&gt;</text>
  <text x="668" y="126" class="card-name">GitHub</text>
  <text x="668" y="143" class="card-handle">@Manabendu-ai</text>
  <text x="794" y="135" class="arrow-icon">➔</text>

  <rect x="390" y="186" width="210" height="84" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1"/>
  <rect x="406" y="216" width="24" height="24" rx="5" fill="#e1306c" opacity="0.2"/>
  <text x="413" y="233" font-family="'Space Grotesk', sans-serif" font-weight="700" font-size="14" fill="#e1306c">IG</text>
  <text x="444" y="224" class="card-name">Instagram</text>
  <text x="444" y="241" class="card-handle">@manabenduu</text>
  <text x="570" y="233" class="arrow-icon">➔</text>

  <rect x="614" y="186" width="210" height="84" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1"/>
  <rect x="630" y="216" width="24" height="24" rx="5" fill="#ff354f" opacity="0.2"/>
  <text x="635" y="233" font-family="'Space Grotesk', sans-serif" font-weight="700" font-size="14" fill="#ff354f">@</text>
  <text x="668" y="224" class="card-name">Direct Email</text>
  <text x="668" y="241" class="card-handle">technoriku@...</text>
  <text x="794" y="233" class="arrow-icon">➔</text>
</svg>"""

with open(os.path.join(ASSETS_DIR, "connect.svg"), "w", encoding="utf-8") as f:
    f.write(connect_svg)

# Update Zip file
zip_path = os.path.join(WORKSPACE, "profile_assets.zip")
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(os.path.join(WORKSPACE, "README.md"), "README.md")
    zipf.write(os.path.join(WORKSPACE, "preview.html"), "preview.html")
    for asset in ["hero.svg", "about-life.svg", "stack.svg", "id-dashboard.svg", "connect.svg"]:
        zipf.write(os.path.join(ASSETS_DIR, asset), os.path.join("assets", asset))

print("Updated profile_assets.zip")
print("--- id-dashboard.svg Typo Fixed Successfully! ---")
