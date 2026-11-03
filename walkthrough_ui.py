import html

import streamlit as st


def render_coachmark(title, message, container=None, placement="bottom"):
    """Show a small animated hint beside the existing control it describes."""
    target = st if container is None else container
    if placement not in {"top", "bottom", "edge", "sidebar"}:
        raise ValueError("placement must be 'top', 'bottom', 'edge', or 'sidebar'")

    target.markdown(
        """
        <style>
        @keyframes coachmark-enter {
            from { opacity: 0; transform: translateY(6px) scale(.99); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }
        .coachmark {
            position: relative;
            margin: .45rem 0 .7rem;
            padding: .75rem .9rem;
            border: 1px solid rgba(125, 178, 255, .26);
            border-radius: 18px 18px 18px 6px;
            background:
                radial-gradient(circle at 100% 0%, rgba(93, 166, 255, .13), transparent 45%),
                var(--secondary-background-color, #1e293b);
            box-shadow: 0 8px 22px rgba(7, 15, 32, .16), inset 0 1px rgba(255, 255, 255, .07);
            color: var(--text-color, inherit);
            animation: coachmark-enter .32s cubic-bezier(.2, .75, .25, 1) both;
        }
        .coachmark--top::before, .coachmark--sidebar::before, .coachmark--bottom::after {
            content: "";
            position: absolute;
            left: 1.15rem;
            width: 10px;
            height: 10px;
            border: 1px solid rgba(125, 178, 255, .26);
            background: var(--secondary-background-color, #1e293b);
            transform: rotate(45deg);
        }
        .coachmark--top::before, .coachmark--sidebar::before {
            top: -6px;
            border-right: 0;
            border-bottom: 0;
        }
        .coachmark--bottom::after {
            bottom: -6px;
            border-left: 0;
            border-top: 0;
        }
        .coachmark--edge { display: none; }
        @media (max-width: 1024px) {
            .coachmark--edge {
                display: block;
                max-width: 20rem;
                margin: .35rem 0 .85rem;
            }
            .coachmark--sidebar { display: none; }
            .coachmark--edge::before {
                content: "";
                position: absolute;
                top: 1rem;
                left: -6px;
                width: 10px;
                height: 10px;
                border-left: 1px solid rgba(125, 178, 255, .26);
                border-bottom: 1px solid rgba(125, 178, 255, .26);
                background: var(--secondary-background-color, #1e293b);
                transform: rotate(45deg);
            }
        }
        .coachmark-title { margin-bottom: .22rem; font-size: .85rem; font-weight: 700; }
        .coachmark-message { font-size: .78rem; line-height: 1.45; opacity: .82; }
        @media (prefers-reduced-motion: reduce) {
            .coachmark { animation: none; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    target.markdown(
        f"""
        <div class="coachmark coachmark--{placement}" role="status">
            <div class="coachmark-title">{html.escape(title)}</div>
            <div class="coachmark-message">{html.escape(message)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
