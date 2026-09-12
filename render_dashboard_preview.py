"""
Render static PNG previews of the dashboard pages (for the README / portfolio).

    python render_dashboard_preview.py

These are matplotlib re-creations of the Streamlit pages built from the same
functions and numbers (startup_analysis.py). They're not browser screenshots.
For real screenshots, run `streamlit run dashboard.py` and capture each page.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch

import startup_analysis as sa

OUT = sa.ROOT / "outputs" / "dashboard"
BLUE, ORANGE, GREY, LIGHT = "#2a6fdb", "#e8833a", "#9aa4b2", "#c9ced6"
INK, MUTED, BG, SIDEBAR = "#1f2430", "#6b7280", "#ffffff", "#f0f2f6"
PAGES = ["Overview", "State Explorer", "Sector Explorer", "Growth Map",
         "Hotspot Finder", "Forecast", "Data & Method"]

plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#d0d4da", "axes.grid": True, "grid.alpha": 0.25,
                     "axes.titlesize": 11, "axes.titleweight": "bold", "axes.titlelocation": "left"})


def frame(active: str, title: str, subtitle: str):
    """Streamlit-like page: sidebar + title. Returns fig and the main-area rect [x0, x1]."""
    fig = plt.figure(figsize=(16, 10), facecolor=BG)
    sb = fig.add_axes([0, 0, 0.17, 1])
    sb.set_facecolor(SIDEBAR); sb.set_xticks([]); sb.set_yticks([]); sb.grid(False)
    for s in sb.spines.values():
        s.set_visible(False)
    sb.text(0.1, 0.95, "🚀 Startup Ecosystem".replace("🚀 ", ""), fontsize=14, weight="bold", color=INK)
    sb.text(0.1, 0.915, "Go to", fontsize=9, color=MUTED)
    for i, p in enumerate(PAGES):
        y = 0.88 - i * 0.04
        on = p == active
        sb.scatter([0.14], [y + 0.007], s=110, transform=sb.transAxes, clip_on=False,
                   facecolor=BLUE if on else "white", edgecolor=BLUE if on else MUTED, lw=1.3)
        sb.text(0.24, y, p, fontsize=10.5, color=INK, weight="bold" if on else "normal")
    sb.set_xlim(0, 1); sb.set_ylim(0, 1)
    sb.text(0.1, 0.46, "Source: DPIIT Startup India\nrecognitions by state x\nindustry x year, 2016-2025\n"
                       "(as of 31 May 2026).\n\nCounts are recognitions,\nnot funding or survival.",
            fontsize=8.5, color=MUTED, va="top", linespacing=1.4)
    fig.text(0.2, 0.945, title, fontsize=22, weight="bold", color=INK)
    fig.text(0.2, 0.915, subtitle, fontsize=11, color=MUTED)
    return fig


def kpis(fig, items, y=0.80, h=0.085):
    n = len(items)
    x0, width, gap = 0.2, 0.77, 0.012
    w = (width - gap * (n - 1)) / n
    for i, (label, value, delta) in enumerate(items):
        ax = fig.add_axes([x0 + i * (w + gap), y, w, h])
        ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
        for s in ax.spines.values():
            s.set_visible(False)
        ax.add_patch(FancyBboxPatch((0.01, 0.03), 0.98, 0.94, boxstyle="round,pad=0,rounding_size=0.06",
                                    transform=ax.transAxes, fc="#fafbfc", ec="#e3e6ea"))
        ax.text(0.06, 0.74, label, fontsize=9.5, color=MUTED, transform=ax.transAxes)
        ax.text(0.06, 0.34, value, fontsize=19, weight="bold", color=INK, transform=ax.transAxes)
        if delta:
            color = "#1a8a4a" if not delta.startswith("-") else "#c0392b"
            ax.text(0.06, 0.1, delta, fontsize=8.5, color=color, transform=ax.transAxes)


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    fig.savefig(path, dpi=110, facecolor=BG)
    plt.close(fig)
    return path


def page_overview(R):
    nat, sy, d, dip = R["national"], R["state_year"], R["decentralisation"], R["dip_2024"]
    fig = frame("Overview", "India's Startup Ecosystem, 2017-2025",
                "Where startups are being created, which sectors are rising, and how fast the map is changing.")
    kpis(fig, [("New recognitions, 2025", f"{nat[2025]:,}", f"+{(nat[2025] / nat[2024] - 1) * 100:.1f}% vs 2024"),
               ("Growth since 2017", f"{nat[2025] / nat[2017]:.1f}x", None),
               ("Top-5 state share", f"{d['top5_end']}%", f"{d['top5_end'] - d['top5_start']:+.1f}pp since 2017"),
               ("States with 1,000+ in 2025", str(int((sy[2025] >= 1000).sum())), None)])

    ax = fig.add_axes([0.2, 0.40, 0.45, 0.33])
    yrs = list(range(2017, 2026))
    ax.bar(yrs, nat[yrs], color=[ORANGE if y == 2024 else BLUE for y in yrs])
    for y in yrs:
        ax.text(y, nat[y], f"{nat[y]:,}", ha="center", va="bottom", fontsize=8)
    ax.set_title("New recognitions per year  (orange = only decline)")
    ax.set_xticks(yrs)

    conc = R["concentration"]
    ax1 = fig.add_axes([0.71, 0.40, 0.23, 0.33])
    ax1.plot(conc["year"], conc["top5_share_pct"], "o-", color=BLUE, ms=4)
    ax1.set_ylabel("Top-5 share (%)", color=BLUE)
    ax2 = ax1.twinx()
    ax2.plot(conc["year"], conc["states_for_80pct"], "s-", color=ORANGE, ms=4)
    ax2.set_ylabel("States needed for 80%", color=ORANGE); ax2.grid(False)
    ax1.set_title("Is it spreading out?")
    ax1.tick_params(axis="x", labelsize=8)

    c = R["convergence"]
    iy = R["industry_year"]
    fig.text(0.2, 0.33, "What the data says", fontsize=14, weight="bold", color=INK)
    bullets = [
        f"Decentralising, slowly: top-5 share fell from {d['top5_start']}% to {d['top5_end']}% "
        f"(Spearman rho vs year = {d['spearman_rho']}).",
        f"The 2024 dip was broad-based: {dip['states_declining']} of {dip['states_considered']} sizeable states fell; "
        f"~{-dip['others_reclassification_effect']} of the {-dip['national_change']} drop was an 'Others' reclassification. "
        f"2025 rebounded {dip['rebound_2025_pct']}%.",
        f"Smaller ecosystems grow faster (rho = {c['spearman_rho']}, p = {c['p_value']:.3f}), "
        f"so growth is shown as CAGR and absolute numbers.",
        f"AI took off: {int(iy.loc['AI', 2022]):,} recognitions in 2022 -> {int(iy.loc['AI', 2025]):,} in 2025.",
    ]
    for i, b in enumerate(bullets):
        fig.text(0.21, 0.29 - i * 0.045, "•  " + b, fontsize=10.5, color=INK)

    ax = fig.add_axes([0.2, 0.04, 0.75, 0.07])
    top = sy[2025].sort_values(ascending=False)
    shares = list(top.head(8).values) + [top.iloc[8:].sum()]
    labels = list(top.head(8).index) + ["Other states"]
    left = 0
    cmap = plt.get_cmap("Set3")
    for i, (v, lab) in enumerate(zip(shares, labels)):
        ax.barh(0, v, left=left, color=cmap(i), edgecolor="white")
        ax.text(left + v / 2, 0, f"{lab}\n{v / top.sum() * 100:.0f}%", ha="center", va="center", fontsize=8)
        left += v
    ax.set_xlim(0, left); ax.axis("off")
    fig.text(0.2, 0.125, "Where 2025's startups came from", fontsize=12, weight="bold", color=INK)
    return save(fig, "01_overview.png")


def page_state(R, state="Karnataka"):
    sy, nat, g = R["state_year"], R["national"], R["state_growth"].loc[state]
    rank = int(sy[2025].rank(ascending=False, method="min")[state])
    fig = frame("State Explorer", "State Explorer", f"Choose a state:  [ {state}  ▾ ]")
    kpis(fig, [("Recognitions 2025", f"{int(g['count_2025']):,}", f"rank #{rank} of {len(sy)}"),
               ("Share of India", f"{g['share_2025_pct']:.1f}%", None),
               ("CAGR 2019-25", f"{g['cagr_2019_2025_pct']:.1f}%", None),
               ("Momentum (CAGR 23-25 minus 19-23)", f"{g['momentum_pp']:+.1f}pp", None)])
    fig.text(0.2, 0.765, f"Segment: {R['segments']['segment'].get(state)}   ·   "
                         f"Industry-mix cluster: {R['clusters']['cluster_name'].get(state)}",
             fontsize=10.5, color="#1c4e9c", bbox=dict(fc="#e8f0fd", ec="none", pad=6))

    yrs = list(range(2017, 2026))
    ax = fig.add_axes([0.2, 0.43, 0.36, 0.29])
    ax.plot(yrs, sy.loc[state, yrs] / sy.loc[state, 2019] * 100, "o-", color=ORANGE, label=state)
    ax.plot(yrs, nat[yrs] / nat[2019] * 100, "o-", color=GREY, label="India")
    ax.set_title("Growth indexed to 2019 = 100"); ax.legend(frameon=False)

    panel = R["panel"]
    rec = panel[(panel["state"] == state) & panel["year"].between(2023, 2025)]
    top = rec.groupby("industry")["startups"].sum().sort_values().tail(10)
    ax = fig.add_axes([0.70, 0.43, 0.27, 0.29])
    ax.barh(top.index, top.values, color=BLUE); ax.set_title("Top 10 sectors, 2023-25")
    ax.tick_params(axis="y", labelsize=8.5)

    lq = R["lq"][R["lq"]["state"] == state].sort_values("lq")
    show = lq.iloc[list(range(min(5, len(lq)))) + list(range(max(len(lq) - 8, 5), len(lq)))]
    ax = fig.add_axes([0.33, 0.05, 0.62, 0.30])
    ax.barh(show["industry"], show["lq"], color=[BLUE if v >= 1 else ORANGE for v in show["lq"]])
    ax.axvline(1, color="black", ls="--", lw=0.8)
    ax.set_title("What this state specialises in (location quotient, 1 = national average)")
    ax.tick_params(axis="y", labelsize=8.5)
    return save(fig, "02_state_explorer.png")


def page_growth_map(R):
    seg = R["segments"]
    med = R["segment_medians"]
    fig = frame("Growth Map", "Growth Map: scale vs acceleration",
                "Right = bigger, up = growth speeding up (CAGR 2023-25 minus CAGR 2019-23). Dashed lines are medians.")
    ax = fig.add_axes([0.2, 0.08, 0.76, 0.78])
    colors = {"Established Leader": BLUE, "Maturing Hub": GREY, "Rising Challenger": ORANGE, "Slowing / Early": LIGHT}
    for name, gg in seg.groupby("segment"):
        ax.scatter(gg["recent_3yr_total"], gg["momentum_pp"], s=gg["count_2025"] / 8 + 40, color=colors[name],
                   label=name, edgecolor="white", alpha=0.9)
    for st_, r in seg.iterrows():
        ax.annotate(st_, (r["recent_3yr_total"], r["momentum_pp"]), fontsize=9, xytext=(0, 9),
                    textcoords="offset points", ha="center")
    ax.set_xscale("log")
    ax.axvline(med["size_median"], ls="--", color="grey", lw=0.8)
    ax.axhline(med["momentum_median"], ls="--", color="grey", lw=0.8)
    ax.set_xlabel("Recognitions 2023-25 (log scale)"); ax.set_ylabel("Momentum (pp)")
    ax.legend(frameon=False, loc="lower left", markerscale=0.6)
    return save(fig, "03_growth_map.png")


def page_hotspots(R):
    hs = R["hotspots"].head(12).iloc[::-1]
    fig = frame("Hotspot Finder", "Hotspot Finder: state × sector",
                "Three separate signals (percentiles) for every state-sector pair with 30+ recognitions in 2023-25.")
    for i, (lab, val) in enumerate([("Scale weight", 33), ("Momentum weight", 33), ("Specialisation weight", 34)]):
        ax = fig.add_axes([0.2 + i * 0.26, 0.80, 0.23, 0.05])
        ax.set_xlim(0, 100); ax.set_ylim(-1, 1); ax.axis("off")
        ax.plot([0, 100], [0, 0], color="#d0d4da", lw=4, solid_capstyle="round")
        ax.plot([0, val], [0, 0], color="#ff4b4b", lw=4, solid_capstyle="round")
        ax.scatter([val], [0], s=90, color="#ff4b4b", zorder=3)
        ax.text(0, 0.9, lab, fontsize=10, color=INK)
        ax.text(val, -0.95, str(val), fontsize=9, color="#ff4b4b", ha="center")
    ax = fig.add_axes([0.36, 0.08, 0.60, 0.66])
    y = np.arange(len(hs))
    for k, (col, c, name) in enumerate([("scale_pct", BLUE, "Scale"), ("momentum_pct", ORANGE, "Momentum"),
                                        ("specialisation_pct", GREY, "Specialisation")]):
        ax.barh(y + (k - 1) * 0.27, hs[col], height=0.26, color=c, label=name)
    ax.set_yticks(y)
    ax.set_yticklabels([f"#{len(hs) - i}  {s} · {ind}  (score {sc:.0f})"
                        for i, (s, ind, sc) in enumerate(zip(hs["state"], hs["industry"], hs["hotspot_score"]))],
                       fontsize=9)
    ax.set_xlim(0, 100); ax.set_xlabel("Percentile")
    ax.set_title("Top 12 by your weights - the three signals side by side")
    ax.legend(frameon=False, loc="lower left", bbox_to_anchor=(0.62, 1.0), ncol=3)
    return save(fig, "04_hotspot_finder.png")


def page_forecast(R):
    nat, bt, fc = R["national"], R["forecast_backtest"], R["forecast"]
    fig = frame("Forecast", "Forecast: how many recognitions in 2026-27?",
                "Four methods trained on 2017-2022, scored on 2023-2025 without seeing those years.")
    kpis(fig, [(f"{y} forecast", f"{fc[y]['point']:,}", f"range {fc[y]['low']:,}-{fc[y]['high']:,}") for y in fc]
         + [("Best holdout MAPE", f"{bt.iloc[0]['mape_pct']}%", bt.iloc[0]["method"])])
    ax = fig.add_axes([0.2, 0.34, 0.76, 0.40])
    hist = nat[nat.index >= 2017]
    yrs = list(fc)
    ax.plot(hist.index, hist.values, "o-", color=BLUE, label="Actual")
    ax.fill_between(yrs, [fc[y]["low"] for y in yrs], [fc[y]["high"] for y in yrs], color=ORANGE, alpha=0.2,
                    label="Range across methods")
    ax.plot([2025] + yrs, [hist[2025]] + [fc[y]["point"] for y in yrs], "o--", color=ORANGE,
            label=f"Forecast: {R['best_method']}")
    ax.set_xticks(list(hist.index) + yrs); ax.legend(frameon=False, loc="upper left")
    ax = fig.add_axes([0.2, 0.05, 0.76, 0.22]); ax.axis("off")
    cols = ["method", "mape_pct", "pred_2023", "pred_2024", "pred_2025"]
    table = ax.table(cellText=bt[cols].astype(str).values,
                     colLabels=["Method", "MAPE %", "Pred 2023", "Pred 2024", "Pred 2025"], loc="center",
                     cellLoc="left")
    table.auto_set_font_size(False); table.set_fontsize(10); table.scale(1, 1.6)
    for (r, _), cell in table.get_celld().items():
        cell.set_edgecolor("#e3e6ea")
        if r == 0:
            cell.set_facecolor(SIDEBAR); cell.set_text_props(weight="bold")
    fig.text(0.2, 0.28, "Holdout backtest   (actual: 2023 = 34,841 · 2024 = 34,294 · 2025 = 49,430)",
             fontsize=12, weight="bold", color=INK)
    return save(fig, "05_forecast.png")


if __name__ == "__main__":
    R = sa.run_all(save=False, verbose=False)
    for f in (page_overview, page_state, page_growth_map, page_hotspots, page_forecast):
        print("saved", f(R).name)
