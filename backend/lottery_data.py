"""Malaysia 4D / Toto lottery historical data + parsing utilities.

Source dataset: imported verbatim from the original Streamlit `HuatPick`/
`Heng Ong Huat` app (`/app/app.py`). Each entry contains the top-3 winners,
10 special prizes and 10 consolation prizes for a single Malaysia 4D draw.

We treat every 4-digit string here as a real-world frequency observation
and use it to derive:
  - digit hot/cold (0..9) for 4D / 5D / 6D games
  - number hot/cold (1..max_n) for Toto pick games, by extracting overlapping
    2-digit substrings inside the valid range.
"""

from collections import Counter
from typing import Dict, List, Tuple
import re

# ---------- BUNDLED HISTORICAL DATA (Feb–Mar 2026) ----------
HISTORICAL_RESULTS: Dict[str, Dict] = {
    "04_02_2026": {"day": "Wednesday", "draw_no": "6085/26", "top_3": ["0338","9428","4436"], "special": ["5850","6843","4529","9745","9153","5908","6119","9136","4981","2416"], "consolation": ["5549","9044","0237","4781","5264","8317","4308","2634","2552","8362"]},
    "07_02_2026": {"day": "Saturday",  "draw_no": "6086/26", "top_3": ["6777","9948","5085"], "special": ["7272","6226","7458","9311","3031","3408","6183","5554","4113","4850"], "consolation": ["5485","2174","9558","6806","6681","4290","1815","5515","8748","3683"]},
    "08_02_2026": {"day": "Sunday",    "draw_no": "6087/26", "top_3": ["1562","0756","5515"], "special": ["7427","0097","2807","3180","8834","9253","2982","0442","5927","1966"], "consolation": ["9211","7149","2060","0205","6473","9711","1256","6317","2634","3378"]},
    "10_02_2026": {"day": "Tuesday",   "draw_no": "6088/26", "top_3": ["9500","0539","4510"], "special": ["4994","2313","7385","9249","5457","0958","3043","8844","6767","1792"], "consolation": ["1363","2810","0334","3569","5633","0251","4804","1459","0167","3805"]},
    "11_02_2026": {"day": "Wednesday", "draw_no": "6089/26", "top_3": ["0444","7857","8826"], "special": ["6906","4964","3627","9475","0876","4744","9337","8835","8012","3462"], "consolation": ["6836","4640","0710","1351","8538","0550","5573","2255","9738","3402"]},
    "14_02_2026": {"day": "Saturday",  "draw_no": "6090/26", "top_3": ["2590","9864","3153"], "special": ["7452","7817","9924","3901","7287","5031","8840","3650","6319","9048"], "consolation": ["2913","8022","4344","2802","2307","8144","2867","5534","0837","5455"]},
    "15_02_2026": {"day": "Sunday",    "draw_no": "6091/26", "top_3": ["8362","3137","0783"], "special": ["8608","2704","1825","7647","0866","8895","2786","5013","3838","5732"], "consolation": ["5403","8002","9963","9898","3786","1991","6342","4698","8018","8222"]},
    "17_02_2026": {"day": "Tuesday",   "draw_no": "6092/26", "top_3": ["5239","7318","3358"], "special": ["8581","7992","0154","0052","7330","7561","9351","7598","7684","5806"], "consolation": ["3046","1820","2827","5548","5442","3541","9402","6094","7822","6992"]},
    "18_02_2026": {"day": "Wednesday", "draw_no": "6093/26", "top_3": ["9991","6676","0430"], "special": ["6986","5661","2702","2371","3392","5426","9461","2350","0986","5029"], "consolation": ["5953","0379","5233","7411","9461","9841","2438","7159","9988","4543"]},
    "21_02_2026": {"day": "Saturday",  "draw_no": "6094/26", "top_3": ["1326","2106","5097"], "special": ["5990","9605","3944","2492","8466","0778","8545","0038","6362","5444"], "consolation": ["3073","6417","9655","0094","0627","4790","1799","5141","3395","0030"]},
    "22_02_2026": {"day": "Sunday",    "draw_no": "6095/26", "top_3": ["3294","6710","7919"], "special": ["3543","8142","0712","7493","9645","0134","3733","3361","8091","6240"], "consolation": ["1927","5797","1468","6862","1125","2022","8886","6717","6476","7419"]},
    "25_02_2026": {"day": "Wednesday", "draw_no": "6096/26", "top_3": ["3814","7343","9748"], "special": ["6903","4138","5411","2241","3034","9657","1290","3887","7524","6502"], "consolation": ["0745","6895","5600","9089","5109","7200","8264","8334","5791","4670"]},
    "28_02_2026": {"day": "Saturday",  "draw_no": "6097/26", "top_3": ["0965","0068","5032"], "special": ["4236","7742","5463","4666","4176","8558","4764","3810","1063","0106"], "consolation": ["0519","7792","6764","5763","1955","7776","2334","6477","9100","5048"]},
    "01_03_2026": {"day": "Sunday",    "draw_no": "6098/26", "top_3": ["6210","0247","9080"], "special": ["9649","0567","9207","5916","7971","0000","2279","9334","8205","2882"], "consolation": ["8229","4742","4000","9979","4509","1781","5788","9259","0232","9483"]},
    "04_03_2026": {"day": "Wednesday", "draw_no": "6099/26", "top_3": ["5347","2165","4113"], "special": ["0824","5196","6745","3410","7453","4351","3057","1883","7812","6668"], "consolation": ["6397","7389","7415","0123","4123","4963","6826","8144","7912","1281"]},
    "07_03_2026": {"day": "Saturday",  "draw_no": "6100/26", "top_3": ["6931","5178","8138"], "special": ["6680","4685","4514","6561","1292","8427","1408","8569","1118","3811"], "consolation": ["3137","3176","3481","5612","7138","8733","4613","7028","1483","0484"]},
    "08_03_2026": {"day": "Sunday",    "draw_no": "6101/26", "top_3": ["7015","0291","4864"], "special": ["6661","9548","4583","9151","5847","3713","1244","9944","5539","9311"], "consolation": ["2903","5022","5314","5778","9261","4239","2305","2626","9097","8712"]},
    "11_03_2026": {"day": "Wednesday", "draw_no": "6102/26", "top_3": ["1563","3185","6942"], "special": ["7242","8773","3120","5527","3299","9563","1346","2368","6598","2698"], "consolation": ["5114","6197","4432","4052","7598","6925","2060","5814","0097","0890"]},
    "14_03_2026": {"day": "Saturday",  "draw_no": "6103/26", "top_3": ["4714","0021","1909"], "special": ["3336","1095","1921","9975","9899","6561","7083","1693","5589","6299"], "consolation": ["0380","9849","4444","1369","1777","1776","8261","3854","3472","5932"]},
    "15_03_2026": {"day": "Sunday",    "draw_no": "6104/26", "top_3": ["5039","0631","3863"], "special": ["2139","2833","0929","1984","8185","1040","2304","0604","1629","9971"], "consolation": ["8758","0929","9610","2269","3220","0397","4602","6487","6356","2293"]},
    "18_03_2026": {"day": "Wednesday", "draw_no": "6105/26", "top_3": ["8047","4206","7103"], "special": ["2868","5044","0350","8483","1805","4440","4175","5938","5864","5520"], "consolation": ["9168","4536","0018","7307","1971","7771","8803","1209","6361","1044"]},
    "21_03_2026": {"day": "Saturday",  "draw_no": "6106/26", "top_3": ["9966","2669","4567"], "special": ["1303","6077","2389","3076","6909","8598","5267","9930","0983","9620"], "consolation": ["4355","8857","6096","6059","3040","1995","8937","6287","8725","3607"]},
    "22_03_2026": {"day": "Sunday",    "draw_no": "6107/26", "top_3": ["2956","6464","3967"], "special": ["7544","2798","7958","4191","3761","9657","3649","5206","8168","7500"], "consolation": ["0954","7262","6881","9389","7216","1451","7934","8093","5091","7653"]},
    "25_03_2026": {"day": "Wednesday", "draw_no": "6108/26", "top_3": ["8666","8159","0185"], "special": ["8702","4804","5338","9042","4548","5537","2358","7768","9713","7457"], "consolation": ["4997","5712","4680","6521","9582","6391","1898","8555","2524","9523"]},
    "28_03_2026": {"day": "Saturday",  "draw_no": "6109/26", "top_3": ["9126","0094","8615"], "special": ["2967","9819","5795","0711","2449","3228","3980","5112","9855","3205"], "consolation": ["7086","8568","5516","1893","2952","1319","3399","4422","1421","4131"]},
}


def all_4d_strings(extra_pool: str = "") -> List[str]:
    """Flatten the bundled dataset + any extra 4-digit strings into a list.

    Args:
        extra_pool: Optional concatenated string of additional 4-digit numbers
                    (e.g. scraped from 4dmoon.com or pasted by an admin).
    """
    pool: List[str] = []
    for entry in HISTORICAL_RESULTS.values():
        pool.extend(entry.get("top_3", []))
        pool.extend(entry.get("special", []))
        pool.extend(entry.get("consolation", []))
    # Pull every length-4 run of digits out of `extra_pool`.
    if extra_pool:
        pool.extend(re.findall(r"\d{4}", extra_pool))
    return pool


def digit_frequencies(pool: List[str]) -> Counter:
    """Returns Counter of digit 0..9 frequencies across all 4-digit strings."""
    c: Counter = Counter()
    for s in pool:
        for ch in s:
            if ch.isdigit():
                c[int(ch)] += 1
    return c


def number_frequencies(pool: List[str], max_n: int) -> Counter:
    """For Toto-style games, extract every 2-digit window (sliding) from each
    4-digit string and keep those falling in [1, max_n]. The 0-padded values
    (e.g. "07") count as 7 — reflecting how Toto numbers are written.

    Example: "5849" → "58","84","49" → kept if within range.
    """
    c: Counter = Counter()
    for s in pool:
        if len(s) < 2:
            continue
        for i in range(len(s) - 1):
            try:
                n = int(s[i:i+2])
            except ValueError:
                continue
            if 1 <= n <= max_n:
                c[n] += 1
        # Also include the last single-digit windowed pair from positions (2,3)
        # which is already covered by the loop above.
    return c


def hot_cold_digits(extra_pool: str = "", top_k: int = 5) -> Dict[str, List[int]]:
    """Return the `top_k` hottest and coldest digits (0..9)."""
    counts = digit_frequencies(all_4d_strings(extra_pool))
    # Ensure all 10 digits present (with 0 count if absent)
    full = [(d, counts.get(d, 0)) for d in range(10)]
    full.sort(key=lambda x: x[1], reverse=True)
    hot = sorted([d for d, _ in full[:top_k]])
    cold = sorted([d for d, _ in full[-top_k:]])
    return {"hot": hot, "cold": cold, "freq": {str(d): n for d, n in full}}


def hot_cold_numbers(max_n: int, extra_pool: str = "", top_k: int = 8) -> Dict[str, List[int]]:
    """Return the `top_k` hottest and coldest numbers in [1, max_n] derived
    from sliding 2-digit windows of the 4D dataset."""
    counts = number_frequencies(all_4d_strings(extra_pool), max_n)
    full = [(n, counts.get(n, 0)) for n in range(1, max_n + 1)]
    full.sort(key=lambda x: x[1], reverse=True)
    hot = sorted([n for n, _ in full[:top_k]])
    cold_pool = [n for n, _ in full if _ == 0] or [n for n, _ in full[-top_k:]]
    cold = sorted(cold_pool[:top_k])
    return {"hot": hot, "cold": cold}


# ---------- LIVE SCRAPER ----------
SCRAPE_URL = "https://www.4dmoon.com/"
SCRAPE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.8",
    "Referer": "https://www.google.com/",
}

# Sports Toto results pages — multiple URLs tried in order.
# These pages list multiple recent draws with 6 winning numbers each.
SPORTSTOTO_URLS: Dict[str, List[str]] = {
    "6_58": [
        "https://en.lottolyzer.com/history/malaysia/sports-toto-6d/6-58",
        "https://4d2u.com/history.php?id=toto658",
    ],
    "6_55": [
        "https://en.lottolyzer.com/history/malaysia/power-toto/6-55",
        "https://4d2u.com/history.php?id=toto655",
    ],
    "6_52": [
        "https://en.lottolyzer.com/history/malaysia/star-toto/6-52",
        "https://4d2u.com/history.php?id=toto652",
    ],
    "6_50": [
        "https://en.lottolyzer.com/history/malaysia/supreme-toto/6-50",
        "https://4d2u.com/history.php?id=toto650",
    ],
}


def scrape_live_4d(timeout: float = 8.0, max_numbers: int = 200) -> List[str]:
    """Best-effort scrape of latest 4-digit numbers from 4dmoon.com.

    Returns up to `max_numbers` four-digit strings. Empty list on failure.
    """
    try:
        import requests
        from bs4 import BeautifulSoup
        r = requests.get(SCRAPE_URL, headers=SCRAPE_HEADERS, timeout=timeout)
        r.raise_for_status()
        text = BeautifulSoup(r.text, "html.parser").get_text(" ", strip=True)
        nums = re.findall(r"\b\d{4}\b", text)
        return nums[:max_numbers]
    except Exception:
        return []


def scrape_sportstoto(game_id: str, max_n: int, max_draws: int = 60, timeout: float = 8.0) -> List[List[int]]:
    """Best-effort scrape of Malaysia Sports Toto results for a specific game.

    Strategy:
      1. Fetch each candidate URL in SPORTSTOTO_URLS[game_id] until one returns
         HTML with at least 6 valid Toto numbers in range.
      2. Extract every 1-2 digit number in range [1, max_n] from the page text.
      3. Group into consecutive chunks of 6 (a single draw is 6 numbers).
      4. Return up to `max_draws` chunks, each a sorted list of 6 unique numbers.

    Returns empty list if no source succeeds.
    """
    urls = SPORTSTOTO_URLS.get(game_id, [])
    if not urls:
        return []

    try:
        import requests
        from bs4 import BeautifulSoup
    except Exception:
        return []

    for url in urls:
        try:
            r = requests.get(url, headers=SCRAPE_HEADERS, timeout=timeout)
            r.raise_for_status()
            text = BeautifulSoup(r.text, "html.parser").get_text(" ", strip=True)
            # Find every 1- or 2-digit number; keep ones in valid range.
            tokens = re.findall(r"\b\d{1,2}\b", text)
            in_range = [int(t) for t in tokens if 1 <= int(t) <= max_n]
            if len(in_range) < 6:
                continue

            draws: List[List[int]] = []
            i = 0
            while i + 6 <= len(in_range) and len(draws) < max_draws:
                chunk = in_range[i:i+6]
                # Treat as valid Toto draw if all 6 numbers are unique AND
                # the spread is wide enough to rule out pagination (1,2,3,4,5,6)
                # or repeated UI counters.
                if (
                    len(set(chunk)) == 6
                    and (max(chunk) - min(chunk)) >= 10
                ):
                    draws.append(sorted(chunk))
                    i += 6
                else:
                    i += 1
            if draws:
                return draws
        except Exception:
            continue

    return []


def hot_cold_from_toto_draws(draws: List[List[int]], max_n: int, top_k: int = 8) -> Dict[str, List[int]]:
    """Compute hot/cold directly from sets of 6-number Toto draws."""
    c: Counter = Counter()
    for draw in draws:
        for n in draw:
            if 1 <= n <= max_n:
                c[n] += 1
    full = [(n, c.get(n, 0)) for n in range(1, max_n + 1)]
    full.sort(key=lambda x: x[1], reverse=True)
    hot = sorted([n for n, _ in full[:top_k]])
    cold_pool = [n for n, _ in full if _ == 0] or [n for n, _ in full[-top_k:]]
    cold = sorted(cold_pool[:top_k])
    return {"hot": hot, "cold": cold}
