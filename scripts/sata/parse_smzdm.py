"""Parse smzdm search-result markdown (both Exa multi-line and Keenable inline
formats) into structured deal records.

Strategy: locate every '##### [title](https://www.smzdm.com/p/ID/' anchor and
slice the text up to the next anchor; extract fields from each slice with
regexes. Works for both output shapes.
"""
import re, os, time

MALLS = ['天猫国际官方直营', '京东全球购', '天猫超市', '天猫精选', '淘宝精选', '淘宝直播',
         '抖音商城', '小米有品', '苏宁易购', '什么值得买', '京东自营', '京喜',
         '京东', '天猫', '淘宝', '拼多多', '唯品会']
ANCHOR_RE = re.compile(r'#####\s*\[([^\]]+)\]\((https://www\.smzdm\.com/p/(\d+)/)')
PRICE_RE = re.compile(r'\[(?:过期\s*\|\s*)?([0-9][0-9,\.]*)\s*元')
DATE_RE = re.compile(r'(\d{2}-\d{2})\s+\d{2}:\d{2}')
TIME_ONLY_RE = re.compile(r'(?<![\d-])(\d{2}:\d{2})(?!\d)')
TAG_RE = re.compile(r'(\d+天新低|历史低价|历史最低|低于常卖价|低于618|低于双11|价格低于618|精选好价)')
CAP_TOKEN_RE = re.compile(r'(\d+(?:\.\d+)?)\s*TB|(\d{2,5})\s*G(?:B)?\b|(?<!\d)(\d)\s*T\b(?![Bb\w])', re.I)


def find_platform(slice_txt):
    """Footer platform: last standalone mall-name occurrence in the slice."""
    best, best_pos = None, -1
    for name in MALLS:
        for m in re.finditer(re.escape(name), slice_txt):
            # standalone = followed by whitespace/end/CJK punctuation, not part of longer mall name
            end = m.end()
            tail = slice_txt[end:end + 2]
            if tail and not re.match(r'[\s\u3000\)\]"。，,]', tail):
                # e.g. 京东红包 / 京东自营 inside text — still accept 京东自营/京东全球购 handled by order
                if name in ('京东', '天猫', '淘宝') and slice_txt[end:end + 2] in ('红包', '自营', '全球', '精选', '超市', '国际'):
                    continue
                if name not in ('京东自营', '京东全球购', '天猫精选', '天猫超市', '淘宝精选'):
                    continue
            if m.start() > best_pos:
                best, best_pos = name, m.start()
    # normalize
    if best == '京东自营':
        best = '京东'
    return best


def extract_capacity(text):
    caps = []
    for m in CAP_TOKEN_RE.finditer(text):
        if m.group(1):
            caps.append(int(float(m.group(1)) * 1000))
        elif m.group(2):
            v = int(m.group(2))
            if 60 <= v <= 16000:
                caps.append(v)
        elif m.group(3):
            caps.append(int(m.group(3)) * 1000)
    caps = [c for c in caps if 60 <= c <= 24000]
    if not caps:
        return None, False
    uniq = sorted(set(caps))
    return uniq[0], len(uniq) > 1


def parse_file(path):
    txt = open(path, encoding='utf-8').read()
    mtime = time.strftime('%m-%d', time.localtime(os.path.getmtime(path)))
    qm = re.match(r'QUERY: (.*)', txt)
    query = qm.group(1).strip() if qm else os.path.basename(path)
    anchors = list(ANCHOR_RE.finditer(txt))
    deals = []
    for idx, a in enumerate(anchors):
        start = a.start()
        end = anchors[idx + 1].start() if idx + 1 < len(anchors) else min(len(txt), start + 2500)
        chunk = txt[start:end]
        title, url, pid = a.group(1), a.group(2), a.group(3)
        pm = PRICE_RE.search(chunk[:600])
        if not pm:
            continue
        price = float(pm.group(1).replace(',', ''))
        if price <= 0 or price > 100000:
            continue
        expired = '过期' in chunk[:200]
        dm = DATE_RE.search(chunk)
        if dm:
            date = dm.group(1)
        elif TIME_ONLY_RE.search(chunk[:1500]):
            date = mtime  # posted "today" at scrape time
        else:
            date = None
        platform = find_platform(chunk)
        tm = TAG_RE.search(chunk[:400])
        cap, ambiguous = extract_capacity(title + ' ' + chunk[:800])
        # description: first sentence with 元/售价 after tags
        desc = ''
        dsm = re.search(r'(?:javascript:;\)\s*)?([^()\[\]]{20,220}(?:售价|实付|到手价|低至)[^()\[\]]{0,120})', chunk[:1600])
        if dsm:
            desc = dsm.group(1).strip()
        deals.append({
            'id': pid, 'title': title.strip(), 'url': url, 'price': price,
            'need_coupon': '需用券' in chunk[:300], 'expired': expired,
            'platform': platform, 'date': date, 'tag': tm.group(1) if tm else None,
            'desc': desc[:200], 'query': query,
            'capacity_gb': cap, 'cap_ambiguous': ambiguous,
        })
    return deals


def all_deals(raw_dir=None):
    if raw_dir is None:
        base = os.environ.get('SATA_RAW_DIR', '/root/.hermes/workspace/sata_scrape')
        raw_dir = base if base.endswith('raw') else os.path.join(base, 'raw')
    deals = {}
    for fn in sorted(os.listdir(raw_dir)):
        if not fn.endswith('.md'):
            continue
        p = os.path.join(raw_dir, fn)
        if os.path.getsize(p) < 4000:
            continue
        try:
            for d in parse_file(p):
                key = d['id']
                old = deals.get(key)
                if old is None:
                    deals[key] = d
                else:
                    # prefer richer record
                    if (old['capacity_gb'] is None and d['capacity_gb']) or \
                       (old['platform'] is None and d['platform']) or \
                       (old['date'] is None and d['date']):
                        merged = dict(old)
                        for f in ('capacity_gb', 'platform', 'date', 'tag', 'desc', 'cap_ambiguous'):
                            if not merged.get(f) and d.get(f):
                                merged[f] = d[f]
                        deals[key] = merged
        except Exception as e:
            print(f"parse error {fn}: {e}")
    out = []
    for d in deals.values():
        d['price_per_gb'] = round(d['price'] / d['capacity_gb'], 3) if d['capacity_gb'] else None
        out.append(d)
    return out


if __name__ == '__main__':
    ds = all_deals()
    print('total:', len(ds))
    from collections import Counter
    print(Counter(d['platform'] for d in ds))
    print('with cap:', sum(1 for d in ds if d['capacity_gb']))
    print('expired:', sum(1 for d in ds if d['expired']))
