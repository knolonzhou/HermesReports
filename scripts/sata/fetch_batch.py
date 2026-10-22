"""Batch fetch smzdm faxian search pages via hermes web_extract.
Usage: python3 fetch_batch.py <n1,n2,...>  -- indices into QUERY_LIST
"""
import os, sys, time, hashlib, urllib.parse, json
from hermes_tools import web_extract

RAW = os.path.join(os.environ.get('SATA_RAW_DIR', '/root/.hermes/workspace/sata_scrape'), 'raw')
os.makedirs(RAW, exist_ok=True)

QUERY_LIST = [
    # SSD
    "SATA固态硬盘", "固态硬盘SATA3", "2.5寸固态硬盘", "固态硬盘1TB SATA", "宏碁固态硬盘",
    "金士顿A400", "英睿达MX500", "三星870EVO", "长城固态硬盘", "朗科固态硬盘",
    "七彩虹固态硬盘", "梵想固态硬盘", "铠侠TC10", "金百达固态硬盘", "达墨固态硬盘",
    "光威固态硬盘", "梅捷固态硬盘", "铭瑄固态硬盘", "京东京造固态硬盘", "海康威视固态硬盘",
    # HDD
    "机械硬盘 SATA", "希捷 机械硬盘", "西数 机械硬盘", "东芝 机械硬盘", "希捷酷鱼",
    "希捷酷狼", "西数蓝盘", "西数紫盘", "西数红盘", "希捷银河",
    "机械硬盘 1TB", "机械硬盘 2TB", "机械硬盘 4TB", "机械硬盘 8TB", "机械硬盘 16TB",
    "东芝MG08", "希捷ST8000", "西数HC550", "监控硬盘", "NAS硬盘",
]

def fetch(q, tries=2):
    qs = urllib.parse.quote(q)
    url = f"https://search.smzdm.com/?c=faxian&s={qs}&order=time&v=b"
    fn = os.path.join(RAW, f"q_{hashlib.md5(q.encode()).hexdigest()[:10]}.md")
    if os.path.exists(fn) and os.path.getsize(fn) > 5000:
        return "CACHED"
    for t in range(tries):
        try:
            r = web_extract([url], char_limit=28000)
            item = r["results"][0]
            c = item.get("content") or ""
            if len(c) > 3000:
                open(fn, "w", encoding="utf-8").write(f"QUERY: {q}\nURL: {url}\n\n{c}")
                return f"OK({len(c)})"
        except Exception:
            pass
        time.sleep(8)
    return "FAIL"

if __name__ == "__main__":
    idxs = [int(x) for x in sys.argv[1].split(",")]
    for i in idxs:
        q = QUERY_LIST[i]
        st = fetch(q)
        print(f"[{i}] {q:20s} {st}", flush=True)
        time.sleep(5)
