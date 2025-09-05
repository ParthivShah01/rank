# Rank_S.py
import streamlit as st
from pathlib import Path
import base64

st.set_page_config(page_title="Current Rank", layout="centered")
st.title("Welcome, Parth!")
st.subheader("Your Current Statistics:")

st.write("Current Rank: D")
st.write("Hunter Type: Assassin")
st.write("XP Points: 1200")
st.write("Villains Defeated: None")

# UI to adjust dims
w = 400
h = 500
bg_mode = "cover"
FRONT = Path("drank.png")
BACK = Path("back.png")

if not FRONT.exists() or not BACK.exists():
    st.error("Make sure 'drank.png' and 'back.png' exist in the same folder as this script.")
    st.stop()

def img_to_data_uri(p: Path) -> str:
    b = p.read_bytes()
    return "data:image/png;base64," + base64.b64encode(b).decode("utf-8")

front_uri = img_to_data_uri(FRONT)
back_uri = img_to_data_uri(BACK)

st.subheader("Your Latest Hunter ID:")
# Inject width/height and background-size into CSS using Python variables
html = f"""
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <style>
      :root{{ --w:{w}px; --h:{h}px; }}
      html,body {{ height: 100%; }}
      body{{ margin:0; background:transparent; display:flex; align-items:center; justify-content:center; height:100%; }}
      .scene {{
        width: var(--w);
        height: var(--h);
        perspective: 1200px;
        margin: 20px auto;
      }}
      .card-inner {{
        width:100%;
        height:100%;
        position:relative;
        transform-style: preserve-3d;
        transition: transform 0.6s cubic-bezier(.2,.8,.2,1);
        border-radius: 16px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.45);
        cursor: pointer;
      }}

      .card-face {{
        position:absolute;
        width:100%;
        height:100%;
        left:0;
        top:0;
        backface-visibility: hidden;
        border-radius: 16px;
        background-size: {bg_mode};
        background-position: center;
      }}

      .front {{
        background-image: url('{front_uri}');
      }}

      .back {{
        background-image: url('{back_uri}');
        transform: rotateY(180deg);
      }}

      .card-inner::after {{
        content: "";
        position:absolute;
        inset:0;
        border-radius:16px;
        pointer-events:none;
        background: linear-gradient(120deg, rgba(255,255,255,0.02), rgba(255,255,255,0.03));
        mix-blend-mode: overlay;
      }}

      @media (max-width:420px){{
        :root{{ --w:300px; --h:430px; }}
      }}
    </style>
  </head>
  <body>
    <div class="scene">
      <div id="cardInner" class="card-inner" tabindex="0" aria-label="flippable card">
        <div class="card-face front"></div>
        <div class="card-face back"></div>
      </div>
    </div>

    <script>
      (function() {{
        const inner = document.getElementById('cardInner');
        let flipped = false;
        let lastTilt = {{ rotX: 0, rotY: 0 }};

        function applyTransform(rotX = 0, rotY = 0) {{
          const flipDeg = flipped ? 180 : 0;
          inner.style.transform = `rotateY(${{flipDeg + rotY}}deg) rotateX(${{rotX}}deg)`;
          lastTilt = {{ rotX, rotY }};
        }}

        inner.addEventListener('click', () => {{
          flipped = !flipped;
          applyTransform(lastTilt.rotX, lastTilt.rotY);
        }});

        inner.addEventListener('mousemove', (e) => {{
          const r = inner.getBoundingClientRect();
          const px = (e.clientX - r.left) / r.width;
          const py = (e.clientY - r.top) / r.height;
          const dx = (px - 0.5) * 2;
          const dy = (py - 0.5) * 2;
          const maxTilt = 10;
          const rotY = dx * maxTilt * 1.1;
          const rotX = -dy * maxTilt;
          applyTransform(rotX, rotY);
        }});

        inner.addEventListener('mouseleave', () => {{
          applyTransform(0, 0);
        }});

        inner.addEventListener('keydown', (e) => {{
          if(e.key === 'Enter' || e.key === ' ') {{
            e.preventDefault();
            flipped = !flipped;
            applyTransform(lastTilt.rotX, lastTilt.rotY);
          }}
        }});

        applyTransform(0, 0);
      }})();
    </script>
  </body>
</html>
"""

# adjust component height so it fits the card + padding
comp_height = h
st.components.v1.html(html, height=comp_height, scrolling=False)











