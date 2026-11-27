#!/usr/bin/env python3
"""Diagrams for blog/transformer-upgrades.html (20 Transformer upgrades). Writes SVGs to assets/diagrams/transformer-upgrades/."""
import os
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'diagrams', 'transformer-upgrades')
CATS = [('norm', 'Normalisation &amp; stability', '#2563eb'), ('pos', 'Position', '#7c3aed'), ('kv', 'Attention &amp; KV cache', '#0d9488'),
        ('sys', 'Speed &amp; serving', '#ea580c'), ('ffn', 'Feed-forward &amp; MoE', '#db2777'), ('obj', 'Training objective', '#16a34a')]
# name, year, category  (year = first paper or first model release that introduced it)
U = [('Pre-LayerNorm', 2019, 'norm'), ('RMSNorm', 2019, 'norm'), ('QK-Norm', 2023, 'norm'), ('Logit soft-capping', 2024, 'norm'),
     ('RoPE', 2021, 'pos'), ('ALiBi', 2021, 'pos'), ('Position interpolation', 2023, 'pos'),
     ('Multi-query attention', 2019, 'kv'), ('Grouped-query attention', 2023, 'kv'), ('Multi-head latent attention', 2024, 'kv'), ('Sliding-window attention', 2020, 'kv'),
     ('FlashAttention', 2022, 'sys'), ('Speculative decoding', 2022, 'sys'), ('PagedAttention', 2023, 'sys'),
     ('SwiGLU', 2020, 'ffn'), ('Parallel attention + FFN', 2021, 'ffn'), ('Mixture of experts', 2017, 'ffn'), ('Load-balancing loss', 2021, 'ffn'), ('Shared + routed experts', 2024, 'ffn'),
     ('Multi-token prediction', 2024, 'obj')]


def timeline():
    W, H, X0, X1, Y0, LH = 1300, 640, 230, 1290, 70, 88
    yrs = range(2017, 2025)
    X = lambda y: X0 + (y - 2017 + 0.4) * (X1 - X0) / 9.6
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Arial,Helvetica,sans-serif">',
         '<rect width="100%" height="100%" fill="#fff"/>',
         '<text x="20" y="34" font-size="22" font-weight="700" fill="#0f172a">20 Transformer upgrades, by year and by what they fix</text>']
    for y in yrs:
        s.append(f'<text x="{X(y):.0f}" y="62" font-size="14" text-anchor="middle" fill="#475569" font-weight="700">{y}</text>')
        s.append(f'<line x1="{X(y):.0f}" y1="68" x2="{X(y):.0f}" y2="{Y0+6*LH}" stroke="#e2e8f0"/>')
    for i, (c, name, col) in enumerate(CATS):
        y = Y0 + i * LH
        s.append(f'<rect x="10" y="{y+6}" width="{X1}" height="{LH-10}" rx="10" fill="{col}" opacity=".07"/>')
        s.append(f'<text x="22" y="{y+LH/2+5}" font-size="15" font-weight="700" fill="{col}">{name}</text>')
        items = [u for u in U if u[2] == c]
        ends = [-1e9, -1e9, -1e9]
        for n, yr, _ in sorted(items, key=lambda u: u[1]):
            cx = X(yr); k = next(i for i, e in enumerate(ends) if cx > e + 6) if any(cx > e + 6 for e in ends) else 2
            ends[k] = cx + 18 + len(n) * 7.2
            cy = y + 24 + k * 23
            s.append(f'<circle cx="{cx:.0f}" cy="{cy}" r="7" fill="{col}"/>')
            s.append(f'<text x="{cx+12:.0f}" y="{cy+5}" font-size="13" fill="#0f172a">{n}</text>')
    s.append(f'<text x="20" y="{H-14}" font-size="12" fill="#64748b">Year = first paper or first model release that introduced the idea (see the article’s sources). Categories are our grouping.</text></svg>')
    return '\n'.join(s)


def kv():
    # KV cache per token, example 64-layer model, 64 query heads of dim 128, BF16 (2 bytes)
    L, H, D, B = 64, 64, 128, 2
    rows = [('Multi-head attention (64 K/V heads)', 2 * H * D * B * L), ('Grouped-query, 8 groups', 2 * 8 * D * B * L),
            ('Multi-query (1 K/V head)', 2 * 1 * D * B * L), ('Latent attention (512 + 64 dims)', (512 + 64) * B * L)]
    mx = rows[0][1]
    s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 330" font-family="Arial,Helvetica,sans-serif">', '<rect width="100%" height="100%" fill="#fff"/>',
         '<text x="20" y="32" font-size="20" font-weight="700" fill="#0f172a">KV cache per token: same model, four attention designs</text>',
         '<text x="20" y="54" font-size="13" fill="#475569">Example: 64 layers, 64 query heads of size 128, 16-bit numbers. Illustrative configuration, our arithmetic.</text>']
    for i, (n, v) in enumerate(rows):
        y = 80 + i * 58; w = 560 * v / mx
        s.append(f'<text x="20" y="{y+24}" font-size="14" fill="#0f172a">{n}</text>')
        s.append(f'<rect x="330" y="{y+6}" width="{max(w,3):.1f}" height="28" rx="5" fill="#0d9488"/>')
        s.append(f'<text x="{340+max(w,3):.0f}" y="{y+26}" font-size="14" font-weight="700" fill="#0f172a">{v/1024:.0f} KB</text>')
    s.append('</svg>')
    return '\n'.join(s)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, '1-timeline.svg'), 'w').write(timeline())
    open(os.path.join(OUT, '2-kv-cache.svg'), 'w').write(kv())
    print('ok')
