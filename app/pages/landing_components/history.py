"""
Historical Dam-Break Events in India Component for JalRakshak Landing Page.
Matches Sections 30, 31, 32, and 48 of the Master Specification.
Features an interactive 3D Coverflow Carousel with real incident images and click-to-inspect dossiers.
"""
from __future__ import annotations
import json
import streamlit as st
import streamlit.components.v1 as components
from app.pages.landing_components.utils import render_html


HISTORICAL_INCIDENTS = [
    {
        "id": "machchhu-1979",
        "name": "Machchhu-II Dam Failure",
        "year": "1979",
        "location": "Morbi, Gujarat",
        "state": "Gujarat",
        "image": "https://upload.wikimedia.org/wikipedia/commons/1/1a/Machchhu_River_watershed.jpg",
        "image_alt": "Machchhu River Basin and Morbi Dam Site",
        "cause": "Extreme monsoon cloudburst (estimated 600 mm in 24 h) producing an unprecedented peak inflow of 14,000 m³/s, overwhelming the spillway design discharge capacity of 6,300 m³/s (overtopping breach).",
        "impact": "A sudden 6-metre flood surge wave cascaded down the Machchhu valley, devastating downstream industrial township Morbi within 20 minutes and washing away low-lying infrastructure.",
        "fatalities": "Estimates vary by source: 1,800 to 25,000 reported fatalities (one of history's deadliest dam failures)",
        "source": "Central Water Commission (CWC) Technical Records & Ministry of Water Resources Inquiry",
        "spillway_gap": "Peak inflow exceeded designed spillway capacity by 222%",
    },
    {
        "id": "panshet-1961",
        "name": "Panshet (Tanajisagar) Dam Failure",
        "year": "1961",
        "location": "Pune, Maharashtra",
        "state": "Maharashtra",
        "image": "https://upload.wikimedia.org/wikipedia/commons/c/cd/Panshet_Dam.JPG",
        "image_alt": "Panshet Dam reservoir embankment near Pune",
        "cause": "Conduit piping erosion and inadequate embankment compaction along the conduit during initial reservoir filling without a reinforced concrete casing.",
        "impact": "The earthen embankment breached within hours, sending a catastrophic surge into the downstream Khadakwasla Dam, damaging its masonry structure and submerging Pune's central municipal districts.",
        "fatalities": "~1,000 reported fatalities (official commission and civil administrative records)",
        "source": "Justice Bawdekar Commission of Inquiry Report (1962)",
        "spillway_gap": "Internal piping failure along unreinforced outlet conduit",
    },
    {
        "id": "tigra-1917",
        "name": "Tigra Dam Failure",
        "year": "1917",
        "location": "Gwalior, Madhya Pradesh",
        "state": "Madhya Pradesh",
        "image": "https://upload.wikimedia.org/wikipedia/commons/2/29/Tighra_Dam_Gwalior.JPG",
        "image_alt": "Tigra Dam masonry structure near Gwalior",
        "cause": "High hydrostatic uplift pressure and geological sliding along horizontal sandstone bedding planes during unprecedented reservoir impoundment.",
        "impact": "Sudden structural sliding displaced the masonry wall, generating flash flooding down the lower Sank River plain that inundated agricultural lands and suburban Gwalior.",
        "fatalities": "~1,000 reported fatalities (historical PWD archives)",
        "source": "Central Water Commission Historical Archives & Gwalior State Documentation",
        "spillway_gap": "Foundation shear failure along weak horizontal sandstone bedding",
    },
    {
        "id": "kaddam-1958",
        "name": "Kaddam Dam Failure & Overtopping",
        "year": "1958 & 1995",
        "location": "Nirmal, Telangana",
        "state": "Telangana",
        "image": "https://images.unsplash.com/photo-1578328819058-b69f3a3b0f6b?w=800&auto=format&fit=crop&q=80",
        "image_alt": "Kaddam Dam Flood Control Embankment and Spillway",
        "cause": "Severe catchment storm generating a peak inflow of 14,700 m³/s, far exceeding the original design discharge capacity of 7,080 m³/s, causing extensive overtopping of composite dykes.",
        "impact": "Overtopping breached both earthen composite flanks, flooding extensive agricultural corridors and downstream villages along the Kaddam and Godavari rivers.",
        "fatalities": "Severe agricultural and property loss; casualties mitigated via downstream telegraph early warnings",
        "source": "Telangana State Irrigation & Command Area Development Department Records",
        "spillway_gap": "Catchment peak inflow exceeded design discharge capacity by 208%",
    },
    {
        "id": "teesta-2023",
        "name": "Chungthang (Teesta-III) Dam Breach",
        "year": "2023",
        "location": "Chungthang, Sikkim",
        "state": "Sikkim",
        "image": "https://upload.wikimedia.org/wikipedia/commons/1/1c/River_Teesta.jpg",
        "image_alt": "Teesta River Gorge and Chungthang Dam Valley",
        "cause": "Glacial Lake Outburst Flood (GLOF) from South Lhonak Lake upstream, funneling an overwhelming debris and water surge that destroyed the 60-metre concrete-faced rockfill dam.",
        "impact": "Catastrophic flash flood swept down the Teesta River gorge, severing highway NH-10 connectivity, washing away 14 bridges, and impacting Chungthang, Dikchu, and Singtam townships.",
        "fatalities": "~100 reported fatalities and missing persons (official disaster relief records)",
        "source": "National Disaster Management Authority (NDMA) & Central Water Commission Reports",
        "spillway_gap": "Glacial outburst surge far exceeded maximum flood design threshold",
    },
]


def render_history() -> None:
    """
    Render historical Indian dam-break incidents with an interactive 3D Coverflow Carousel.
    When any slide is clicked, the dossier below updates to display that incident's technical details.
    """
    render_html("<div id='history' style='padding-top: 50px;'></div>")

    render_html(
        """
        <div style="text-align: center; max-width: 800px; margin: 0 auto 24px auto;">
            <div style="font-size: 0.8rem; font-weight: 600; color: #B8423A; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px;">
                06 · HISTORICAL PRECEDENTS
            </div>
            <h2 style="font-size: 2.3rem; font-weight: 600; color: #17324D; margin: 0 0 12px 0;">
                Learn From Historical Dam-Break Events
            </h2>
            <p style="font-size: 1.05rem; color: #68747D; line-height: 1.6;">
                Examine documented Indian dam failures to calibrate scenario parameters, understand breach triggers, and validate inundation models.
            </p>
            <div style="display: inline-block; background: #FFFFFF; border: 1px solid #D7DDE1; border-radius: 20px; padding: 4px 14px; font-size: 0.8rem; color: #256B8E; font-weight: 600; margin-top: 6px;">
                👆 Click any incident card or use arrow controls to inspect historical dossier
            </div>
        </div>
        """
    )

    incidents_json = json.dumps(HISTORICAL_INCIDENTS)

    # 3D Coverflow Carousel component with synchronized technical dossier below
    carousel_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}
            body {{
                font-family: 'IBM Plex Sans', -apple-system, sans-serif;
                background-color: transparent;
                color: #1E252B;
                user-select: none;
                overflow: hidden;
            }}
            :root {{
                --cf-card: clamp(200px, 26vw, 300px);
                --perspective: calc(var(--cf-card) * 3);
            }}
            .carousel-wrapper {{
                width: 100%;
                position: relative;
                padding: 10px 0 20px 0;
            }}
            .stage-container {{
                position: relative;
                width: 100%;
                overflow: hidden;
                cursor: grab;
                outline: none;
                perspective: var(--perspective);
                touch-action: pan-y;
                padding: 24px 0;
            }}
            .stage-container:active {{
                cursor: grabbing;
            }}
            .cards-track {{
                position: relative;
                height: calc(var(--cf-card) * 0.95);
                transform-style: preserve-3d;
            }}
            .card {{
                position: absolute;
                left: 50%;
                top: 0;
                width: var(--cf-card);
                height: 100%;
                border-radius: 12px;
                overflow: hidden;
                background: #FFFFFF;
                border: 1px solid #D7DDE1;
                box-shadow: 0 12px 28px rgba(23, 50, 77, 0.14);
                cursor: pointer;
                transition: box-shadow 0.2s ease;
                will-change: transform, opacity;
            }}
            .card:hover {{
                box-shadow: 0 16px 36px rgba(23, 50, 77, 0.22);
            }}
            .card img {{
                width: 100%;
                height: 100%;
                object-fit: cover;
                display: block;
                pointer-events: none;
            }}
            .card-overlay {{
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                background: linear-gradient(180deg, transparent 0%, rgba(15, 23, 42, 0.85) 50%, rgba(15, 23, 42, 0.98) 100%);
                padding: 14px 12px 10px 12px;
                color: #FFFFFF;
            }}
            .card-badge {{
                display: inline-block;
                background: #B8423A;
                color: #FFFFFF;
                font-family: 'IBM Plex Mono', monospace;
                font-size: 11px;
                font-weight: 700;
                padding: 2px 7px;
                border-radius: 4px;
                margin-bottom: 4px;
                letter-spacing: 0.5px;
            }}
            .card-title {{
                font-size: 14px;
                font-weight: 700;
                line-height: 1.25;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }}
            .card-subtitle {{
                font-size: 11.5px;
                color: #5FA8D3;
                margin-top: 2px;
                font-family: 'IBM Plex Mono', monospace;
            }}
            .nav-btn {{
                position: absolute;
                top: 38%;
                transform: translateY(-50%);
                z-index: 200;
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background: #FFFFFF;
                border: 1px solid #D7DDE1;
                color: #17324D;
                font-size: 20px;
                font-weight: bold;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(23, 50, 77, 0.12);
                transition: all 0.15s ease;
            }}
            .nav-btn:hover {{
                background: #F7F8F6;
                color: #256B8E;
                transform: translateY(-50%) scale(1.08);
            }}
            .nav-prev {{ left: 16px; }}
            .nav-next {{ right: 16px; }}
            .dots-container {{
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 8px;
                margin: 4px 0 16px 0;
            }}
            .dot {{
                width: 9px;
                height: 9px;
                border-radius: 50%;
                background: #D7DDE1;
                cursor: pointer;
                transition: all 0.2s ease;
            }}
            .dot.active {{
                background: #17324D;
                width: 22px;
                border-radius: 5px;
            }}

            /* Dossier Card Container */
            .dossier-card {{
                background: #FFFFFF;
                border: 1px solid #D7DDE1;
                border-top: 4px solid #B8423A;
                border-radius: 8px;
                padding: 22px 24px;
                margin-top: 10px;
                box-shadow: 0 4px 14px rgba(23, 50, 77, 0.04);
                transition: opacity 0.25s ease, transform 0.25s ease;
            }}
            .dossier-header {{
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 12px;
                border-bottom: 1px solid #E5E8EB;
                padding-bottom: 10px;
                flex-wrap: wrap;
                gap: 8px;
            }}
            .dossier-title {{
                font-size: 1.35rem;
                font-weight: 700;
                color: #17324D;
            }}
            .dossier-meta-badge {{
                background: rgba(184, 66, 58, 0.1);
                color: #B8423A;
                border: 1px solid rgba(184, 66, 58, 0.3);
                font-family: 'IBM Plex Mono', monospace;
                font-size: 0.85rem;
                font-weight: 700;
                padding: 4px 10px;
                border-radius: 4px;
            }}
            .dossier-location {{
                font-size: 0.9rem;
                color: #256B8E;
                font-weight: 600;
                margin-bottom: 14px;
            }}
            .dossier-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 16px;
                margin-bottom: 14px;
            }}
            @media (max-width: 640px) {{
                .dossier-grid {{
                    grid-template-columns: 1fr;
                }}
            }}
            .dossier-section-title {{
                font-size: 0.72rem;
                font-weight: 700;
                color: #17324D;
                letter-spacing: 0.06em;
                text-transform: uppercase;
                margin-bottom: 4px;
            }}
            .dossier-text {{
                font-size: 0.88rem;
                color: #68747D;
                line-height: 1.5;
            }}
            .dossier-alert {{
                background: #F7F8F6;
                border: 1px solid #D7DDE1;
                border-left: 3px solid #B8423A;
                padding: 10px 14px;
                border-radius: 4px;
                margin-bottom: 12px;
            }}
            .dossier-footer {{
                border-top: 1px solid #E5E8EB;
                padding-top: 10px;
                font-size: 0.76rem;
                color: #68747D;
                display: flex;
                justify-content: space-between;
                flex-wrap: wrap;
                gap: 8px;
            }}
        </style>
    </head>
    <body>
        <div class="carousel-wrapper">
            <div class="stage-container" id="frame">
                <div class="cards-track" id="track"></div>
            </div>

            <button class="nav-btn nav-prev" id="btnPrev" aria-label="Previous incident">‹</button>
            <button class="nav-btn nav-next" id="btnNext" aria-label="Next incident">›</button>

            <div class="dots-container" id="dots"></div>

            <!-- Technical Dossier rendered below the pictures when clicked -->
            <div class="dossier-card" id="dossier">
                <div class="dossier-header">
                    <div>
                        <div class="dossier-title" id="dossierTitle"></div>
                        <div class="dossier-location" id="dossierLocation"></div>
                    </div>
                    <div class="dossier-meta-badge" id="dossierYear"></div>
                </div>

                <div class="dossier-grid">
                    <div>
                        <div class="dossier-section-title">PRIMARY FAILURE MECHANISM / HYDRAULIC CAUSE</div>
                        <div class="dossier-text" id="dossierCause"></div>
                    </div>
                    <div>
                        <div class="dossier-section-title">INUNDATION & VALLEY PROPAGATION IMPACT</div>
                        <div class="dossier-text" id="dossierImpact"></div>
                    </div>
                </div>

                <div class="dossier-alert">
                    <div class="dossier-section-title" style="color: #B8423A;">REPORTED CASUALTIES & FATALITIES</div>
                    <div class="dossier-text" style="color: #17324D; font-weight: 600; font-family: 'IBM Plex Mono', monospace;" id="dossierFatalities"></div>
                </div>

                <div class="dossier-footer">
                    <div><b>DATA ATTRIBUTION:</b> <span id="dossierSource"></span></div>
                    <div style="font-family: 'IBM Plex Mono', monospace; color: #256B8E;" id="dossierSpillway"></div>
                </div>
            </div>
        </div>

        <script>
            const incidents = {incidents_json};
            const count = incidents.length;

            const rotate = 44;
            const depth = 0.6;
            const falloff = 0.56;
            const fade = 0.12;
            const gap = 0.08;

            let pos = 0;
            let target = 0;
            let width = 0;
            let rafId = null;
            let selected = 0;

            const frame = document.getElementById('frame');
            const track = document.getElementById('track');
            const dotsContainer = document.getElementById('dots');
            const btnPrev = document.getElementById('btnPrev');
            const btnNext = document.getElementById('btnNext');

            // Elements in Dossier
            const dossierTitle = document.getElementById('dossierTitle');
            const dossierLocation = document.getElementById('dossierLocation');
            const dossierYear = document.getElementById('dossierYear');
            const dossierCause = document.getElementById('dossierCause');
            const dossierImpact = document.getElementById('dossierImpact');
            const dossierFatalities = document.getElementById('dossierFatalities');
            const dossierSource = document.getElementById('dossierSource');
            const dossierSpillway = document.getElementById('dossierSpillway');

            const cardElements = [];

            // Build DOM cards and dots
            incidents.forEach((item, idx) => {{
                const card = document.createElement('div');
                card.className = 'card';
                card.innerHTML = `
                    <img src="${{item.image}}" alt="${{item.image_alt}}" draggable="false" />
                    <div class="card-overlay">
                        <span class="card-badge">${{item.year}}</span>
                        <div class="card-title">${{item.name}}</div>
                        <div class="card-subtitle">${{item.location}}</div>
                    </div>
                `;
                card.addEventListener('click', () => {{
                    goTo(idx);
                }});
                track.appendChild(card);
                cardElements.push(card);

                const dot = document.createElement('div');
                dot.className = 'dot' + (idx === 0 ? ' active' : '');
                dot.addEventListener('click', () => goTo(idx));
                dotsContainer.appendChild(dot);
            }});

            function updateDossier(idx) {{
                const ev = incidents[idx];
                dossierTitle.textContent = ev.name;
                dossierLocation.textContent = '📍 ' + ev.location + ' · State of ' + ev.state;
                dossierYear.textContent = ev.year;
                dossierCause.textContent = ev.cause;
                dossierImpact.textContent = ev.impact;
                dossierFatalities.textContent = ev.fatalities;
                dossierSource.textContent = ev.source;
                dossierSpillway.textContent = ev.spillway_gap;

                // Update dots
                Array.from(dotsContainer.children).forEach((d, i) => {{
                    d.className = 'dot' + (i === idx ? ' active' : '');
                }});
            }}

            function paint() {{
                if (!width) width = cardElements[0].offsetWidth;
                if (!width) return;
                const pitch = width * (1 + gap);

                cardElements.forEach((card, index) => {{
                    let offset = index - pos;
                    offset = ((offset % count) + count) % count;
                    if (offset > count / 2) offset -= count;

                    const distance = Math.abs(offset);
                    const ramp = Math.pow(distance, falloff);
                    const tilt = Math.min(rotate * ramp, 82) * Math.sign(offset);

                    card.style.transform = `translateX(calc(-50% + ${{offset * pitch}}px)) ` +
                                          `translateZ(${{-depth * width * ramp}}px) rotateY(${{-tilt}}deg)`;
                    
                    const edge = Math.min(1, Math.max(0, count / 2 - distance));
                    card.style.opacity = Math.max(0, 1 - fade * distance) * edge;
                    card.style.zIndex = Math.round(100 - distance);
                }});
            }}

            function indexAt(p) {{
                return ((Math.round(p) % count) + count) % count;
            }}

            function settle(newTarget) {{
                if (rafId !== null) cancelAnimationFrame(rafId);
                target = newTarget;
                selected = indexAt(target);
                updateDossier(selected);

                function step() {{
                    const remaining = target - pos;
                    if (Math.abs(remaining) < 0.0004) {{
                        pos = target;
                        paint();
                        rafId = null;
                        return;
                    }}
                    pos += remaining * 0.16;
                    paint();
                    rafId = requestAnimationFrame(step);
                }}
                rafId = requestAnimationFrame(step);
            }}

            function goTo(idx) {{
                const cur = indexAt(target);
                let diff = idx - cur;
                if (diff > count / 2) diff -= count;
                if (diff < -count / 2) diff += count;
                settle(target + diff);
            }}

            function nudge(dir) {{
                settle(target + dir);
            }}

            btnPrev.addEventListener('click', () => nudge(-1));
            btnNext.addEventListener('click', () => nudge(1));

            // Drag / Pointer gestures
            let drag = null;
            frame.addEventListener('pointerdown', (e) => {{
                if (rafId !== null) cancelAnimationFrame(rafId);
                frame.setPointerCapture(e.pointerId);
                target = pos;
                drag = {{
                    x: e.clientX,
                    pos: pos,
                    v: 0,
                    t: performance.now()
                }};
            }});

            frame.addEventListener('pointermove', (e) => {{
                if (!drag) return;
                const pitch = width * (1 + gap);
                const now = performance.now();
                const prev = pos;
                pos = drag.pos - (e.clientX - drag.x) / pitch;
                drag.v = ((pos - prev) / Math.max(now - drag.t, 1)) * 1000;
                drag.t = now;

                const curIdx = indexAt(pos);
                if (curIdx !== selected) {{
                    selected = curIdx;
                    updateDossier(selected);
                }}
                paint();
            }});

            const endDrag = () => {{
                if (!drag) return;
                const carried = Math.max(-2, Math.min(2, drag.v * 0.18));
                drag = null;
                settle(Math.round(pos + carried));
            }};

            frame.addEventListener('pointerup', endDrag);
            frame.addEventListener('pointercancel', endDrag);

            window.addEventListener('resize', () => {{
                if (cardElements[0]) width = cardElements[0].offsetWidth;
                paint();
            }});

            // Initial load
            setTimeout(() => {{
                if (cardElements[0]) width = cardElements[0].offsetWidth;
                updateDossier(0);
                paint();
            }}, 50);
        </script>
    </body>
    </html>
    """

    components.html(carousel_html, height=720, scrolling=False)
