"""Generate the expanded markdown report from the deals dataset.
Env: SATA_DATE (YYYY-MM-DD, default today), SATA_RAW_DIR (raw page dir for stats).
Fully dynamic: month filter, counts, champions, recommendations."""
import json, sys, os, glob, time
from collections import defaultdict, Counter

DATE = os.environ.get('SATA_DATE') or time.strftime('%Y-%m-%d')
MONTH = DATE[5:7]  # e.g. '10'
REPO = '/root/HermesReports'
rows = json.load(open(f'{REPO}/data/{DATE}-sata-deals.json'))

RAW_DIR = os.environ.get('SATA_RAW_DIR', '/root/.hermes/workspace/sata_scrape')
if not RAW_DIR.endswith('raw'):
    RAW_DIR = os.path.join(RAW_DIR, 'raw')
PAGES = len([f for f in glob.glob(os.path.join(RAW_DIR, '*.md')) if os.path.getsize(f) > 4000])


def band(cap):
    if cap <= 130: return '128G'
    if cap <= 260: return '256G'
    if cap <= 520: return '512G'
    if cap <= 1100: return '1TB'
    if cap <= 2100: return '2TB'
    if cap <= 4100: return '4TB'
    if cap <= 8200: return '8TB'
    return '16TB+'

BANDS = ['128G', '256G', '512G', '1TB', '2TB', '4TB', '8TB', '16TB+']

month_rows = [r for r in rows if r.get('date') and r['date'][:2] == MONTH]
good = [r for r in month_rows if r['capacity_gb'] and r.get('plausible')]


def dedupe(g):
    ded = {}
    for r in g:
        k = r['title'][:30]
        if k not in ded or r['price'] < ded[k]['price'] or \
           (r['price'] == ded[k]['price'] and (r['date'] or '') > (ded[k]['date'] or '')):
            ded[k] = r
    return sorted(ded.values(), key=lambda x: (x['price_per_gb'], x['price']))


groups = defaultdict(list)
for r in good:
    groups[(r['category'], band(r['capacity_gb']))].append(r)

L = []
L.append(f"# SATA3.0 固态硬盘 & 机械硬盘 全网比价大数据报告（{DATE}）\n")
L.append("> 本报告基于 **什么值得买多平台好价数据库** 程序化抓取解析生成，覆盖京东、天猫/淘宝、拼多多、抖音商城等平台的真实成交爆料价。")
L.append(f"> 原始好价记录 **{len(rows)} 条**（去重后），其中 {MONTH} 月记录 **{len(month_rows)} 条**，可计入单价排行的有效记录 **{len(good)} 条**。")
L.append(f"> 机器可读数据：`data/{DATE}-sata-deals.csv` / `.json`\n")
L.append("## 数据概览\n")
plat = Counter(r['platform'] or '未知' for r in month_rows)
cat = Counter(r['category'] for r in month_rows)
L.append("| 维度 | 分布 |")
L.append("|---|---|")
L.append(f"| {MONTH}月记录平台分布 | " + "、".join(f"{k} {v} 条" for k, v in plat.most_common()) + " |")
L.append(f"| 品类分布（{MONTH}月） | " + "、".join(f"{'固态硬盘' if k == 'SSD' else '机械硬盘'} {v} 条" for k, v in cat.most_common()) + " |")
L.append(f"| 时间跨度 | {min((r['date'] or '99') for r in rows)} ~ {max((r['date'] or '') for r in rows)} |")
L.append("")
L.append("> ⚠️ **行情背景**：2026 年存储处于涨价周期——NAND 颗粒合约价一年涨约 5 倍（$0.05→$0.26/GB，什么值得买 10 月日报），机械盘同步大涨。大促期间部分型号略有回落，刚需逢「历史低价/天新低」标记出手，非刚需可比价后等下一波。\n")

L.append("---\n\n# 第一部分：SATA3.0 固态硬盘（SSD）完整榜单\n")
for b in BANDS:
    g = dedupe(groups.get(('SSD', b), []))
    if not g: continue
    L.append(f"\n## SSD · {b} 档（{len(g)} 款去重后）\n")
    L.append("| 序 | 日期 | 平台 | 商品 | 容量 | 到手价 | 元/GB | 好价标记 |")
    L.append("|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(g, 1):
        cp = '（需用券）' if r['need_coupon'] else ''
        tag = f"🔥{r['tag']}" if r['tag'] else ''
        L.append(f"| {i} | {r['date']} | {r['platform'] or '—'} | [{r['title'][:56]}]({r['url']}) | {r['capacity_gb']}GB | ¥{r['price']:g}{cp} | **{r['price_per_gb']:.3f}** | {tag} |")

L.append("\n---\n\n# 第二部分：SATA3.0 机械硬盘（HDD）完整榜单\n")
for b in BANDS:
    g = dedupe(groups.get(('HDD', b), []))
    if not g: continue
    L.append(f"\n## HDD · {b} 档（{len(g)} 款去重后）\n")
    L.append("| 序 | 日期 | 平台 | 商品 | 容量 | 到手价 | 元/GB | 好价标记 |")
    L.append("|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(g, 1):
        cp = '（需用券）' if r['need_coupon'] else ''
        tag = f"🔥{r['tag']}" if r['tag'] else ''
        L.append(f"| {i} | {r['date']} | {r['platform'] or '—'} | [{r['title'][:56]}]({r['url']}) | {r['capacity_gb']}GB | ¥{r['price']:g}{cp} | **{r['price_per_gb']:.3f}** | {tag} |")

L.append("\n---\n\n# 第三部分：分平台观察\n")
byplat = defaultdict(list)
for r in good:
    byplat[r['platform'] or '未知'].append(r)
for p in ['京东', '天猫精选', '拼多多', '抖音商城', '淘宝精选', '京东全球购', '天猫超市', '京喜', '小米有品', '苏宁易购']:
    g = byplat.get(p)
    if not g: continue
    g2 = dedupe(g)
    best = min(g2, key=lambda x: x['price_per_gb'])
    L.append(f"\n## {p}（有效记录 {len(g)} 条，去重 {len(g2)} 款）\n")
    L.append(f"- 全场每 GB 最低：**{best['title'][:50]}** {best['capacity_gb']}GB ¥{best['price']:g}（{best['price_per_gb']:.3f} 元/GB，{best['date']}）")
    for c, label in (('SSD', '固态'), ('HDD', '机械')):
        gg = dedupe([r for r in g if r['category'] == c])[:3]
        if gg:
            L.append(f"- {label}最值 TOP3：" + "；".join(f"{r['title'][:26]}… {r['capacity_gb']}GB ¥{r['price']:g}" for r in gg))

# ---- Part 4: champions & dynamic recommendations ----
L.append("\n---\n\n# 第四部分：结论与购买建议\n")
L.append(f"## 🏆 各容量档性价比冠军（{MONTH} 月实价，下单前核实）\n")
champs = []
for c, label in (('SSD', '固态硬盘'), ('HDD', '机械硬盘')):
    for b in ['128G', '256G', '512G', '1TB', '2TB', '4TB', '8TB', '16TB+']:
        g = dedupe(groups.get((c, b), []))
        if not g: continue
        champs.append((c, label, b, g[0]))
L.append("| 品类 | 容量档 | 冠军商品 | 到手价 | 元/GB | 平台/日期 |")
L.append("|---|---|---|---|---|---|")
for c, label, b, r in champs:
    cp = '（需用券）' if r['need_coupon'] else ''
    L.append(f"| {label} | {b} | [{r['title'][:48]}]({r['url']}) | ¥{r['price']:g}{cp} | **{r['price_per_gb']:.3f}** | {r['platform'] or '—'} {r['date']} |")

L.append("\n## 💡 一句话建议（自动生成）\n")
for c, label, b, r in champs:
    if b not in ('512G', '1TB', '4TB'):
        continue
    g = dedupe(groups.get((c, b), []))
    runner = f"；次选 {g[1]['title'][:30]}… ¥{g[1]['price']:g}（{g[1]['platform']}）" if len(g) > 1 else ''
    tag = f"，🔥{r['tag']}" if r['tag'] else ''
    L.append(f"- **SATA {label} {b}** → {r['platform'] or '—'}「{r['title'][:40]}」¥{r['price']:g}（{r['price_per_gb']:.3f} 元/GB{tag}）{runner}")

L.append("""
## ⚠️ 避坑清单（通用）

1. **涨价周期慎囤**：NAND 合约价一年内 $0.05→$0.26/GB，零售端水涨船高；只认「天新低/低于 618」标记的好价出手。
2. **杂牌风险**：近期实锤案例——精亿盘 20 天不认盘且 400 电话欠费停服；梵想盘主控损坏靠专业设备救回。白牌盘只放非重要数据，重要数据认准宏碁/金士顿/铠侠/致态/西数/希捷及京东自营渠道。
3. **「非全新/白盘」= 二手翻新**：好评率再高也别存重要数据。
4. **SMR 叠瓦盘**：希捷酷鱼 4TB（ST4000DM004）、西数蓝盘部分型号是 SMR，只适合读多写少；NAS/RAID 必须 CMR（银河 Exos、酷狼、红盘 Plus、紫盘、企业级）。
5. **M.2 SATA ≠ NVMe**：M.2 接口走 SATA 总线的盘速度仍是 ~550MB/s，老笔记本升级前确认主板协议。
6. **京东全球购无国内联保**：大容量盘便宜 20-30%，但售后走海外渠道，谨慎评估。

## 📋 数据说明
""".replace('{MONTH}', MONTH))
L.append(f"- 数据来源：什么值得买（smzdm）好价频道，程序化抓取 {PAGES} 个搜索页（按品牌 × 容量 × 平台过滤组合），解析出 {len(rows)} 条去重好价，本报告采用其中 {MONTH} 月且价格合理的 {len(good)} 条。")
L.append("- 「元/GB」= 到手价 ÷ 标称容量；「好价标记」来自爆料页历史低价标签（如 704 天新低 = 近两年最低）。")
L.append("- 淘宝/京东/拼多多/抖音站内对未登录爬虫有登录墙；好价爆料页是能同时覆盖四平台真实到手价的公开数据源，平台字段取自爆料页脚注商城标签。")
L.append("- 价格为爆料时刻到手价，大促期间变动快，**下单前务必点开链接核实**。")

L.append("\n---\n")
L.append("### 附录：完整数据文件\n")
L.append(f"- CSV（Excel 可直接打开）：[data/{DATE}-sata-deals.csv](https://github.com/knolonzhou/HermesReports/blob/main/data/{DATE}-sata-deals.csv)")
L.append(f"- JSON（程序可读）：[data/{DATE}-sata-deals.json](https://github.com/knolonzhou/HermesReports/blob/main/data/{DATE}-sata-deals.json)")
L.append(f"\n*报告由 Hermes Agent 自动生成 · 抓取/解析/排行全流程程序化 · {DATE}*")

p = f'{REPO}/reports/{DATE}-sata-storage-deals-bigdata.md'
open(p, 'w', encoding='utf-8').write('\n'.join(L))
print("report written:", p, os.path.getsize(p), "bytes;",
      f"{len(rows)} rows, {len(month_rows)} this month, {len(good)} ranked, {PAGES} pages")
