#!/usr/bin/env python3
"""Generate shuige-course HTML pages with DeepSeek API content"""
import os, json, urllib.request, time

API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
API_URL = "https://api.deepseek.com/v1/chat/completions"

CSS = """<style>:root{--bg:#07070a;--gold:#e2b64f;--card:#121218;--text:#e0e0e0;--text2:#a0a0ab;--text3:#656570;--border:#22222d;--accent:#f59e0b}*{margin:0;padding:0;box-sizing:border-box}body{background:var(--bg);color:var(--text);font-family:'Noto Serif SC',Georgia,serif;line-height:1.9}.nav{position:sticky;top:0;z-index:100;background:rgba(7,7,10,.95);backdrop-filter:blur(10px);border-bottom:1px solid var(--border);padding:1rem 2rem;display:flex;justify-content:space-between;align-items:center}.nav a{color:var(--text2);text-decoration:none;margin-left:1.5rem;font-size:.9rem;transition:color .2s}.nav a:hover,.nav a.active{color:var(--gold)}.nav .logo{color:var(--gold);font-size:1.2rem;font-weight:700}.container{max-width:800px;margin:0 auto;padding:3rem 2rem}h1{font-size:2rem;color:var(--gold);margin-bottom:.5rem}h2{font-size:1.4rem;color:var(--gold);margin:2rem 0 1rem;padding-bottom:.5rem;border-bottom:1px solid var(--border)}h3{font-size:1.1rem;color:var(--text);margin:1.5rem 0 .8rem}p{margin-bottom:1.2rem;color:var(--text2);font-size:1rem}blockquote{border-left:3px solid var(--gold);padding:1rem 1.5rem;margin:1.5rem 0;background:var(--card);color:var(--text);font-style:italic;border-radius:0 8px 8px 0}.exercise{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1.5rem;margin:2rem 0}.exercise h3{color:var(--gold);margin-top:0}.exercise ol{margin-left:1.5rem;color:var(--text2)}.exercise li{margin-bottom:.8rem}.bottom-nav{display:flex;justify-content:space-between;align-items:center;padding:2rem;border-top:1px solid var(--border);margin-top:3rem}.bottom-nav a{color:var(--gold);text-decoration:none}.meta{color:var(--text3);font-size:.85rem;margin-bottom:2rem}.card-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1.5rem;margin:2rem 0}.course-card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:1.5rem;transition:all .3s;text-decoration:none;display:block}.course-card:hover{border-color:var(--gold);transform:translateY(-2px)}.course-card .num{color:var(--gold);font-size:.85rem;font-weight:700}.course-card h3{color:var(--text);margin:.5rem 0}.course-card p{color:var(--text3);font-size:.9rem;margin:0}.hero{text-align:center;padding:4rem 2rem}.hero h1{font-size:2.5rem;margin-bottom:1rem}.hero p{font-size:1.1rem;max-width:600px;margin:0 auto;color:var(--text3)}.quote-rotator{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:2rem;margin:2rem 0;text-align:center}.quote-rotator blockquote{border:none;background:transparent;font-size:1.2rem}@media(max-width:768px){.container{padding:2rem 1rem}h1{font-size:1.5rem}.card-grid{grid-template-columns:1fr}}</style>"""

NAV = """<nav class="nav"><div><a href="index.html" class="logo">🏛️ 水哥课程</a></div><div><a href="index.html">课程首页</a><a href="lesson1.html">第1课</a><a href="lesson5.html">第5课</a><a href="lesson10.html">第10课</a></div></nav>"""

COURSES = [
    (1, "微观辨水——超强观察力的养成", "从520杯水中辨出指定的那一杯，王昱珩用近乎神迹的表现征服了全中国。这个被称作'水哥'的男人，他的观察力究竟从何而来？",
     ["童年的显微镜：一个不走寻常路的孩子", "520杯水的神话：微观辨水的技术拆解", "观察力的三层修炼法：注意→辨别→记忆", "从水到万物：观察力如何迁移到一切领域"],
     ["回顾你今天注意到的三件最细微的事物，描述它们的特征",
      "尝试'微观辨物'练习：准备10杯水，记住其中一杯的细微特征，打乱后找出",
      "思考：你的专业领域里，哪些细节是外行人完全看不到但你一眼就能发现的？"]),
    (2, "清华往事——天才不需要合群", "高考专业第一、清华美院学霸——但水哥的成长轨迹与'别人家的孩子'完全不同。自闭症、不愿说话、被母亲严厉管教……",
     ["不是神童，是'问题儿童'：水哥的另类童年", "自闭症与美术：当沉默成为表达", "清华的孤独天才：为什么他不需要社交认可", "高考前的人生哲学：玩三年，考第一"],
     ["你在学校时期是'合群者'还是'独行者'？这对你后来有什么影响？",
      "如果让你重新度过学生时代，你会改变自己的社交方式吗？",
      "水哥说'天才不需要合群'——你同意吗？什么情况下合群是必要的？"]),
    (3, "我不需要朋友——独处的力量", "在圆桌派的访谈中，水哥直言'我根本不需要朋友'。这句话让窦文涛、马未都都沉默了。但水哥并非反社会——他对独处的理解，恰恰是当代人最稀缺的智慧。",
     ["圆桌派上的惊人之语：水哥为什么说不需要朋友", "独处≠孤独：重新定义'一个人'的价值", "植物教会我的事：从养花到养心", "深度工作的秘密：为什么最好的创造发生在独处时"],
     ["计算你一周中真正'独处'的时间（不刷手机、不社交媒体的独处）——有多少？",
      "尝试一次'数字排毒'：关机半天，用纸笔记录你的想法和感受",
      "水哥通过养植物获得平静——找一个你能沉浸其中的'无目的爱好'"]),
]

def call_deepseek(prompt, max_tokens=4000):
    """Call DeepSeek API to generate content"""
    data = json.dumps({
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是康波研究院的课程撰写专家。请用流畅优美的中文撰写课程内容，风格参考《圆桌派》式的深度对话风格，既有知识密度又不失可读性。每段200-400字，包含具体案例、数据或引文。使用HTML段落标签<p>包裹每段。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8,
        "max_tokens": max_tokens
    }).encode()
    
    req = urllib.request.Request(API_URL, data=data, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    })
    
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read())
        return result["choices"][0]["message"]["content"]

def build_page(num, title, subtitle, section_titles, exercises):
    """Build a complete course HTML page"""
    prev_num = num - 1 if num > 1 else None
    next_num = num + 1 if num < 10 else None
    prev_html = f'<a href="lesson{prev_num}.html">← 上一课</a>' if prev_num else '<span></span>'
    next_html = f'<a href="lesson{next_num}.html">下一课 →</a>' if next_num else '<span></span>'
    
    # Generate sections
    sections_html = ""
    for i, sec_title in enumerate(section_titles):
        prompt = f"""请为课程《{title}》撰写第{i+1}节内容。

课程：第{num}课「{title}」
本节标题：{sec_title}
本节副标题：{subtitle}

要求：
1. 写600-800字的中文内容
2. 包含至少1个具体案例或故事
3. 包含至少1处可以加粗的关键观点（用<strong>标签）
4. 包含1-2句'水哥式'的犀利语录（用<blockquote>标签引用）
5. 语言风格：深度但不学究，像窦文涛《圆桌派》的聊天质感

请直接输出HTML格式的内容（多个<p>段落+<blockquote>引用），不要写标题。"""
        
        try:
            content = call_deepseek(prompt, 2000)
            sections_html += f'<h2>{sec_title}</h2>\n{content}\n'
            time.sleep(1)  # Rate limit
        except Exception as e:
            sections_html += f'<h2>{sec_title}</h2>\n<p>本节内容生成中...（{e}）</p>\n'
    
    # Exercises
    ex_html = '<div class="exercise"><h3>💡 思考练习</h3><ol>'
    for ex in exercises:
        ex_html += f'<li>{ex}</li>'
    ex_html += '</ol></div>'
    
    # Kangbo connection
    kc_html = f"""<h2>🔗 康波关联</h2>
<p>本课所讲的'{title}'主题与康波周期的关联在于：每一个时代的创新者和独行者，往往出现在周期的低谷期——正如第五轮康波萧条期（2015-2025）中，水哥这样不随波逐流的个体反而获得了最大的关注。当旧秩序瓦解、新范式尚未确立时，<strong>独立思考者成为稀缺资源</strong>。</p>"""
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>第{num}课：{title} - 水哥王昱珩：独行者的智慧</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Inter:wght@400;500&display=swap" rel="stylesheet">
{CSS}
</head>
<body>
{NAV}
<div class="container">
<h1>第{num}课：{title}</h1>
<p class="meta">{subtitle}</p>
{sections_html}
{ex_html}
{kc_html}
</div>
<div class="bottom-nav">
{prev_html}
<a href="index.html">📚 课程首页</a>
{next_html}
</div>
</body>
</html>"""
    return html

# Generate courses 1-3
base = "/root/shuige-course"
os.makedirs(base, exist_ok=True)

for num, title, subtitle, sections, exercises in COURSES:
    fpath = os.path.join(base, f"lesson{num}.html")
    if os.path.exists(fpath):
        print(f"lesson{num}.html already exists, skipping")
        continue
    print(f"Generating lesson{num}: {title}...")
    html = build_page(num, title, subtitle, sections, exercises)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  -> {fpath} ({len(html)} chars)")
    time.sleep(1)

print("Done with batch 1 (courses 1-3)")
