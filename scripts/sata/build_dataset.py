"""Build the final comparison dataset + markdown report from raw smzdm pages."""
import sys, json, re, os, csv
from collections import defaultdict, Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, parse_smzdm
importlib.reload(parse_smzdm)

REPO = '/root/HermesReports'
import time as _t
DATE = os.environ.get('SATA_DATE') or _t.strftime('%Y-%m-%d')

SSD_KW = re.compile(r'(固态|SSD|ssd)')
HDD_KW = re.compile(r'(机械硬盘|机械|HDD|酷鱼|酷狼|酷鹰|蓝盘|紫盘|红盘|银河|Exos|企业级|监控盘|监控硬盘|垂直盘|空气盘|氦气)')
# portable / accessory — not internal SATA drives
EXCLUDE_KW = re.compile(r'(硬盘盒|移动硬盘|便携|PSSD|U盘|优盘|type-?c|Type-?C|USB3\.0|USB 3\.0|usb3|扩展坞|内存条|散热器|支架|数据线|易驱线|光驱位|硬盘座|底座|扩展|NAS整机|服务器整机)', re.I)
SATA_HINT = re.compile(r'(SATA|sata|Sata|2\.5英寸|2\.5寸|3\.5英寸|3\.5寸|串口)')
CAP_RE = re.compile(r'(\d+(?:\.\d+)?)\s*TB|(\d{2,5})\s*GB|(\d{2,5})\s*G(?![BHz])|(?<!\d)(\d)\s*T(?![Bb\w])', re.I)


def capacities_in(text):
    caps = set()
    for m in CAP_RE.finditer(text):
        g = m.group(1) or m.group(2) or m.group(3) or m.group(4)
        if m.group(1):
            v = int(float(m.group(1)) * 1000)
        elif m.group(2) or m.group(3):
            v = int(g)
        elif m.group(4):
            v = int(m.group(4)) * 1000
        else:
            continue
        if 60 <= v <= 24000:
            caps.add(v)
    return sorted(caps)


def classify(d):
    t = d['title']
    if EXCLUDE_KW.search(t):
        return None, None, True
    is_ssd = bool(SSD_KW.search(t))
    is_hdd = bool(HDD_KW.search(t))
    if not (is_ssd or is_hdd):
        return None, None, False
    cat = 'SSD' if is_ssd else 'HDD'
    # internal-SATA filter: SSD must mention SATA/2.5" or must NOT mention NVMe/M.2/PCIe
    nvme = re.search(r'(NVMe|nvme|NVME|PCIe|PCIE|pcie|M\.2|M2接口|ngff|NGFF|固态硬盘\s*M\.2)', t)
    sata = SATA_HINT.search(t)
    if cat == 'SSD' and nvme and not sata:
        return None, None, False
    if cat == 'SSD' and not sata and not nvme:
        # no interface info at all — keep only if query context was SATA-ish
        if not re.search(r'(SATA|sata|2\.5)', d.get('query', '') or ''):
            return None, None, False
    # capacity from TITLE only (desc has variant noise)
    caps = capacities_in(t)
    if not caps:
        desc_head = d.get('desc', '')[:100]
        # skip variant-range text like "128GB-2TB多种容量"
        if not re.search(r'(\d+\s*G\s*[-~至]\s*\d+|多种容量|\d+G?/?\d+T)', desc_head):
            caps = capacities_in(desc_head)
    cap = caps[0] if len(caps) == 1 else None
    ambiguous = len(caps) > 1
    return cat, cap, ambiguous


ds = parse_smzdm.all_deals()
rows = []
for d in ds:
    if d['expired']:
        continue
    cat, cap, ambiguous = classify(d)
    if cat is None:
        continue
    d['category'] = cat
    d['capacity_gb'] = cap
    d['cap_ambiguous'] = bool(ambiguous) and cap is None
    d['price_per_gb'] = round(d['price'] / cap, 3) if cap else None
    # plausibility gate: SSD 0.15~12 ¥/GB, HDD 0.05~1.5 ¥/GB
    if d['price_per_gb'] is not None:
        lo, hi = (0.15, 12) if cat == 'SSD' else (0.05, 1.5)
        d['plausible'] = lo <= d['price_per_gb'] <= hi
    else:
        d['plausible'] = None
    rows.append(d)

byid = {}
for d in rows:
    k = d['id']
    if k not in byid:
        byid[k] = d
    else:
        old = byid[k]
        for f in ('capacity_gb', 'platform', 'date', 'tag', 'desc'):
            if not old.get(f) and d.get(f):
                old[f] = d[f]
        if old.get('price_per_gb') is None and d.get('price_per_gb') is not None:
            old['price_per_gb'] = d['price_per_gb']
            old['capacity_gb'] = d['capacity_gb']
rows = list(byid.values())

os.makedirs(f'{REPO}/data', exist_ok=True)
with open(f'{REPO}/data/{DATE}-sata-deals.json', 'w', encoding='utf-8') as f:
    json.dump(rows, f, ensure_ascii=False, indent=1)

fields = ['category','platform','date','title','capacity_gb','cap_ambiguous','price','price_per_gb','plausible','need_coupon','tag','url']
with open(f'{REPO}/data/{DATE}-sata-deals.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for d in sorted(rows, key=lambda x: (x['category'], x['date'] or '')):
        w.writerow({k: d.get(k) for k in fields})

print("classified rows:", len(rows))
print(Counter((d['category'], d['platform']) for d in rows))
print("with single capacity:", sum(1 for d in rows if d['capacity_gb']))
print("ambiguous:", sum(1 for d in rows if d['cap_ambiguous']))
print("implausible:", sum(1 for d in rows if d.get('plausible') is False))
print("date range:", min(d['date'] or '99' for d in rows), "->", max(d['date'] or '00' for d in rows))
