"""Reusable HTML fragments for the Streamlit UI."""

from __future__ import annotations

import html


def hearing_loader_markup(title: str, detail: str) -> str:
    """Animated lawyer holding justice scales while long-running work executes."""
    t = html.escape(title)
    d = html.escape(detail)
    return f"""
<div class="court-hearing-loader-wrap" role="status" aria-live="polite">
  <svg width="200" height="168" viewBox="0 0 200 168" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
    <rect x="22" y="152" width="156" height="5" rx="2" fill="#2e3046"/>
    <g class="ch-lawyer-group">
      <path d="M78 52 L122 52 L132 148 L68 148 Z" fill="#1e2a4a" stroke="#2e4060" stroke-width="1.2"/>
      <path d="M92 52 L100 64 L108 52" fill="#e8e4d9"/>
      <g transform="translate(100, 50)">
        <g class="ch-scales">
          <line x1="0" y1="6" x2="0" y2="42" stroke="#e8e4d9" stroke-width="2.2" stroke-linecap="round"/>
          <polygon points="0,-2 -5,6 5,6" fill="#f0c96b" stroke="##c9a227" stroke-width="0.8"/>
          <line x1="-34" y1="6" x2="34" y2="6" stroke="#c9a227" stroke-width="2.6" stroke-linecap="round"/>
          <line x1="-28" y1="6" x2="-28" y2="24" stroke="#b8922e" stroke-width="1.3"/>
          <line x1="28" y1="6" x2="28" y2="24" stroke="#b8922e" stroke-width="1.3"/>
          <path d="M-40 27 Q-28 36 -16 27" fill="none" stroke="#c9a227" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M16 27 Q28 36 40 27" fill="none" stroke="#c9a227" stroke-width="1.5" stroke-linecap="round"/>
          <ellipse cx="-28" cy="29" rx="11" ry="4.5" fill="#f0c96b" fill-opacity="0.14" stroke="#c9a227" stroke-width="1.2"/>
          <ellipse cx="28" cy="29" rx="11" ry="4.5" fill="#f0c96b" fill-opacity="0.14" stroke="#c9a227" stroke-width="1.2"/>
        </g>
      </g>
      <circle cx="100" cy="34" r="16" fill="#d4a574" stroke="#2e3046" stroke-width="1"/>
      <path d="M86 28 Q100 17 114 28" fill="#1a1510"/>
    </g>
  </svg>
  <div class="ch-loader-title">{t}</div>
  <div class="ch-loader-detail">{d}</div>
  <div class="ch-loader-dots" aria-hidden="true"><span></span><span></span><span></span></div>
</div>
"""
