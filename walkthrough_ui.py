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
            border-radius: 18px 18px 18px 6px;
            animation: coachmark-enter .32s cubic-bezier(.2, .75, .25, 1) both;
        }
        .coachmark-theme-light, .coachmark[data-coachmark-theme="light"] {
            background: #ffffff !important;
            border: 1px solid #26384f !important;
            box-shadow: 0 8px 22px rgba(25, 45, 75, .12), inset 0 1px rgba(255, 255, 255, .9);
            color: #111111 !important;
        }
        .coachmark-theme-dark, .coachmark[data-coachmark-theme="dark"] {
            background: #1e293b !important;
            border: 1px solid rgba(125, 178, 255, .3) !important;
            box-shadow: 0 8px 22px rgba(7, 15, 32, .22), inset 0 1px rgba(255, 255, 255, .07);
            color: #f3f6fc !important;
        }
        .coachmark-theme-system, .coachmark[data-coachmark-theme="light"] {
            background: #ffffff !important;
            border: 1px solid #26384f !important;
            box-shadow: 0 8px 22px rgba(25, 45, 75, .12), inset 0 1px rgba(255, 255, 255, .9);
            color: #111111 !important;
        }
        @media (prefers-color-scheme: dark) {
            .coachmark-theme-system, .coachmark[data-coachmark-theme="dark"] {
                background: #1e293b !important;
                border-color: rgba(125, 178, 255, .3) !important;
                box-shadow: 0 8px 22px rgba(7, 15, 32, .22), inset 0 1px rgba(255, 255, 255, .07);
                color: #f3f6fc !important;
            }
        }
        .coachmark-title, .coachmark-message { color: inherit !important; }
        .coachmark--top::before, .coachmark--sidebar::before, .coachmark--bottom::after {
            content: "";
            position: absolute;
            left: 1.15rem;
            width: 10px;
            height: 10px;
            transform: rotate(45deg);
        }
        .coachmark[data-coachmark-theme="light"].coachmark--top::before,
        .coachmark[data-coachmark-theme="light"].coachmark--sidebar::before,
        .coachmark[data-coachmark-theme="light"].coachmark--bottom::after,
        .coachmark[data-coachmark-theme="light"].coachmark--edge::before,
        .coachmark-theme-light.coachmark--top::before,
        .coachmark-theme-light.coachmark--sidebar::before,
        .coachmark-theme-light.coachmark--bottom::after,
        .coachmark-theme-light.coachmark--edge::before,
        .coachmark-theme-system.coachmark--top::before,
        .coachmark-theme-system.coachmark--sidebar::before,
        .coachmark-theme-system.coachmark--bottom::after,
        .coachmark-theme-system.coachmark--edge::before {
            border: 1px solid #26384f;
            background: #ffffff;
        }
        .coachmark[data-coachmark-theme="dark"].coachmark--top::before,
        .coachmark[data-coachmark-theme="dark"].coachmark--sidebar::before,
        .coachmark[data-coachmark-theme="dark"].coachmark--bottom::after,
        .coachmark[data-coachmark-theme="dark"].coachmark--edge::before,
        .coachmark-theme-dark.coachmark--top::before,
        .coachmark-theme-dark.coachmark--sidebar::before,
        .coachmark-theme-dark.coachmark--bottom::after,
        .coachmark-theme-dark.coachmark--edge::before {
            border: 1px solid rgba(125, 178, 255, .3);
            background: #1e293b;
        }
        .coachmark-theme-light.coachmark--top::before,
        .coachmark-theme-light.coachmark--sidebar::before,
        .coachmark-theme-system.coachmark--top::before,
        .coachmark-theme-system.coachmark--sidebar::before {
            border-right: 0;
            border-bottom: 0;
        }
        .coachmark-theme-light.coachmark--bottom::after,
        .coachmark-theme-system.coachmark--bottom::after {
            border-left: 0;
            border-top: 0;
        }
        .coachmark-theme-dark.coachmark--top::before,
        .coachmark-theme-dark.coachmark--sidebar::before {
            border-right: 0;
            border-bottom: 0;
        }
        .coachmark-theme-dark.coachmark--bottom::after {
            border-left: 0;
            border-top: 0;
        }
        .coachmark-theme-light.coachmark--edge::before,
        .coachmark-theme-system.coachmark--edge::before {
            border-top: 0;
            border-right: 0;
        }
        .coachmark-theme-dark.coachmark--edge::before {
            border-top: 0;
            border-right: 0;
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
                border-left: 1px solid currentColor;
                border-bottom: 1px solid currentColor;
                transform: rotate(45deg);
            }
        }
        @media (prefers-color-scheme: dark) {
            .coachmark-theme-system.coachmark--top::before,
            .coachmark-theme-system.coachmark--sidebar::before,
            .coachmark-theme-system.coachmark--bottom::after,
            .coachmark-theme-system.coachmark--edge::before {
                border-color: rgba(125, 178, 255, .3);
                background: #1e293b;
            }
        }
        .coachmark-title { margin-bottom: .22rem; font-size: .85rem; font-weight: 700; }
        .coachmark-message { font-size: .78rem; line-height: 1.45; }
        @media (prefers-reduced-motion: reduce) {
            .coachmark { animation: none; }
        }
        /* Repaint immediately when Streamlit's native theme toggle changes. */
        .coachmark[data-coachmark-theme="light"], [data-theme="light"] .coachmark {
            background: #ffffff !important;
            border-color: #26384f !important;
            box-shadow: 0 8px 22px rgba(25, 45, 75, .12), inset 0 1px rgba(255, 255, 255, .9) !important;
            color: #111111 !important;
        }
        .coachmark[data-coachmark-theme="light"] .coachmark-title,
        .coachmark[data-coachmark-theme="light"] .coachmark-message,
        [data-theme="light"] .coachmark-title,
        [data-theme="light"] .coachmark-message { color: #111111 !important; }
        .coachmark[data-coachmark-theme="dark"], [data-theme="dark"] .coachmark {
            background: #1e293b !important;
            border-color: rgba(125, 178, 255, .3) !important;
            box-shadow: 0 8px 22px rgba(7, 15, 32, .22), inset 0 1px rgba(255, 255, 255, .07) !important;
            color: #f3f6fc !important;
        }
        .coachmark[data-coachmark-theme="dark"] .coachmark-title,
        .coachmark[data-coachmark-theme="dark"] .coachmark-message,
        [data-theme="dark"] .coachmark-title,
        [data-theme="dark"] .coachmark-message { color: #f3f6fc !important; }
        .coachmark[data-coachmark-theme="light"].coachmark--top::before,
        .coachmark[data-coachmark-theme="light"].coachmark--sidebar::before,
        .coachmark[data-coachmark-theme="light"].coachmark--bottom::after,
        .coachmark[data-coachmark-theme="light"].coachmark--edge::before,
        [data-theme="light"] .coachmark.coachmark--top::before,
        [data-theme="light"] .coachmark.coachmark--sidebar::before,
        [data-theme="light"] .coachmark.coachmark--bottom::after,
        [data-theme="light"] .coachmark.coachmark--edge::before {
            border-color: #26384f !important;
            background: #ffffff !important;
        }
        .coachmark[data-coachmark-theme="dark"].coachmark--top::before,
        .coachmark[data-coachmark-theme="dark"].coachmark--sidebar::before,
        .coachmark[data-coachmark-theme="dark"].coachmark--bottom::after,
        .coachmark[data-coachmark-theme="dark"].coachmark--edge::before,
        [data-theme="dark"] .coachmark.coachmark--top::before,
        [data-theme="dark"] .coachmark.coachmark--sidebar::before,
        [data-theme="dark"] .coachmark.coachmark--bottom::after,
        [data-theme="dark"] .coachmark.coachmark--edge::before {
            border-color: rgba(125, 178, 255, .3) !important;
            background: #1e293b !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    target.markdown(
        f"""
        <div class="coachmark coachmark--{placement} coachmark-theme-system" role="status">
            <div class="coachmark-title">{html.escape(title)}</div>
            <div class="coachmark-message">{html.escape(message)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    target.iframe(
        """
        <script>
        (() => {
            const app = window.parent;
            const doc = app.document;
            const applyTheme = () => {
                const nodes = [
                    doc.querySelector('[data-testid="stAppViewContainer"]'),
                    doc.querySelector('.stApp'),
                    doc.body,
                ].filter(Boolean);
                let bg = '';
                for (const node of nodes) {
                    const candidate = app.getComputedStyle(node).backgroundColor;
                    if (candidate && !candidate.includes('rgba(0, 0, 0, 0)')) {
                        bg = candidate;
                        break;
                    }
                }
                const match = bg.match(/[0-9.]+/g);
                let theme = 'light';
                if (match && match.length >= 3) {
                    const [r, g, b] = match.slice(0, 3).map(Number);
                    const luminance = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255;
                    theme = luminance < 0.5 ? 'dark' : 'light';
                } else if (app.matchMedia('(prefers-color-scheme: dark)').matches) {
                    theme = 'dark';
                }
                doc.querySelectorAll('.coachmark').forEach((card) => {
                    if (card.dataset.coachmarkTheme !== theme) {
                        card.dataset.coachmarkTheme = theme;
                    }
                });
            };
            applyTheme();
            const observer = new MutationObserver(applyTheme);
            observer.observe(doc.documentElement, {
                attributes: true,
                childList: true,
                characterData: true,
                subtree: true,
                attributeFilter: ['class', 'style', 'data-theme'],
            });
        })();
        </script>
        """,
        width=1,
        height=1,
        tab_index=-1,
    )
