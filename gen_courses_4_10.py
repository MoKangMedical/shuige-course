#!/usr/bin/env python3
"""Generate courses 4-10 + index.html using DeepSeek API"""
import os, json, urllib.request, time

API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
API_URL = "https://api.deepseek.com/v1/chat/completions"

CSS = """<style>:root{--bg:#07070a;--gold:#e2b64f;--card:#121218;--text:#e0e0e0;--text2:#a0a0ab;--text3:#656570;--border:#22222d;--accent:#f59e0b}*{margin:0;padding:0;box-sizing:border-box}body{background:var(--bg);color:var(--text);font-family:'Noto Serif SC',Georgia,serif;line-height:1.9}.nav{position:sticky;top:0;z-index:100;background:rgba(7,7,10,.95);backdrop-filter:blur(10px);border-bottom:1px solid var(--border);padding:1rem 2rem;display:flex;justify-content:space-between;align-items:center}.nav a{color:var(--text2);text-decoration:none;margin-left:1.5rem;font-size:.9rem;transition:color .2s}.nav a:hover,.nav a.active{color:var(--gold)}.nav .logo{color:var(--gold);font-size:1.2rem;font-weight:700}.container{max-width:800px;margin:0 auto;padding:3rem 2rem}h1{font-size:2rem;color:var(--gold);margin-bottom:.5rem}h2{font-size:1.4rem;color:var(--gold);margin:2rem 0 1rem;padding-bottom:.5rem;border-bottom:1px solid var(--border)}h3{font-size:1.1rem;color:var(--text);margin:1.5rem 0 .8rem}p{margin-bottom:1.2rem;color:var(--text2);font-size:1rem}blockquote{border-left:3px solid var(--gold);padding:1rem 1.5rem;margin:1.5rem 0;background:var(--card);color:var(--text);font-style:italic;border-radius:0 8px 8px 0}.exercise{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1.5rem;margin:2rem 0}.exercise h3{color:var(--gold);margin-top:0}.exercise ol{margin-left:1.5rem;color:var(--text2)}.exercise li{margin-bottom:.8rem}.bottom-nav{display:flex;justify-content:space-between;align-items:center;padding:2rem;border-top:1px solid var(--border);margin-top:3rem}.bottom-nav a{color:var(--gold);text-decoration:none}.meta{color:var(--text3);font-size:.85rem;margin-bottom:2rem}.card-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1.5rem;margin:2rem 0}.course-card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:1.5rem;transition:all .3s;text-decoration:none;display:block}.course-card:hover{border-color:var(--gold);transform:translateY(-2px)}.course-card .num{color:var(--gold);font-size:.85rem;font-weight:700}.course-card h3{color:var(--text);margin:.5rem 0}.course-card p{color:var(--text3);font-size:.9rem;margin:0}.hero{text-align:center;padding:4rem 2rem}.hero h1{font-size:2.5rem;margin-bottom:1rem}.hero p{font-size:1.1rem;max-width:600px;margin:0 auto;color:var(--text3)}@media(max-width:768px){.container{padding:2rem 1rem}h1{font-size:1.5rem}.card-grid{grid-template-columns:1fr}}</style>"""

NAV = """<nav class="nav"><div><a href="index.html" class="logo">🏛️ 水哥课程</a></div><div><a href="index.html">课程首页</a><a href="lesson1.html">第1课</a><a href="lesson5.html">第5课</a><a href="lesson10.html">第10课</a></div></nav>"""

COURSES_4_10 = [
    (4, "婚姻的真相——两个独立个体的契约", "在圆桌派的访谈中，水哥直言自己和妻子的关系'全是假的'。这句话震惊了窦文涛和马未都。但仔细听下去会发现，他不是在否定婚姻——他在重新定义婚姻。",
     ["圆桌派上的婚姻宣言：为什么说'全是假的'", "两个独立个体的契约：婚姻不是合二为一", "经济独立与情感独立的双重自由", "当代婚姻的第三条路：不离婚也不将就"],
     ["你如何看待'婚姻是两个独立个体的契约'这个观点？与传统的'执子之手与子偕老'有何不同？",
      "水哥说和妻子的关系'全是假的'——你觉得他说的'假'指什么？真的婚姻应该是什么样？",
      "在当代中国，'不婚主义'和'丁克'越来越普遍。你认为是社会进步还是退化？"]),
    (5, "自闭症到鬼才之眼——神经多样性的礼物", "水哥在初高中时曾患谱系自闭症，不愿说话，神经敏感。绘画是唯一的表达方式。但正是这段'不正常'的经历，造就了他超凡的观察力。",
     ["被误解的天赋：自闭症不是缺陷，是另一种操作系统", "神经敏感的超能力：当噪音变成信息", "绘画：沉默者的语言", "重新定义'正常'：为什么世界需要不同的大脑"],
     ["你有没有被贴过'不合群''性格古怪'的标签？这些标签多大程度上反映真实的你？",
      "如果'正常'只是统计上的多数，那'不正常'是否应该被'治疗'？",
      "水哥的案例让我们重新思考'神经多样性'。你的独特之处是什么？它给你带来了什么？"]),
    (6, "用眼睛破案——观察力如何改变现实", "2015年，王昱珩凭借一段模糊的监控视频，协助山东警方破获了一起肇事逃逸案。他用肉眼从监控中提取出了连技术手段都难以获取的信息。这不是超能力——这是观察力的现实应用。",
     ["监控视频中的福尔摩斯：如何从模糊画面中提取关键信息", "警方的求助：当技术手段走到尽头", "观察力的降维打击：从二维到三维的还原", "你也可以的'破案式'观察训练"],
     ["试着在街上观察一个路人的30秒，然后写下你能回忆的所有细节。和同伴对比，看看谁注意到了更多。",
      "水哥协助破案的故事说明，观察力可以救人。你能想到你所在行业中，观察力可以创造什么价值吗？",
      "如果有机会，你想用水哥的观察力去做什么？"]),
    (7, "植物的智慧——从养动植物中学习生命", "水哥的家是一个'植物园'：从热带雨林到沙漠植物，从微藻到兰花。他说植物教会他的东西，比任何人都多。一个不愿与人交往的人，如何在植物世界找到了最深的连接？",
     ["被植物治愈的人生：'和花说话比和人说话容易'", "植物的哲学：等待、扎根、向阳", "从养花到养心：为什么现代人需要一棵植物", "水哥的植物清单：哪些植物最适合陪伴独处者"],
     ["你有没有养过植物？你觉得养植物和养宠物有什么不同的体验？",
      "水哥说'植物教会我等待'。在这个追求即时满足的时代，你最近一次'等待'是什么？",
      "选一株植物养一个月，记录它的变化，同时记录你自己的心绪变化。"]),
    (8, "人机大战——当最强人类大脑遇到AI", "2017年《最强大脑》第四季，王昱珩作为中国队队长参加了人机大战。当人类最强观察力遇到了人工智能的图像识别——这场对决不仅是技术的较量，更是一场关于'什么是智慧'的哲学辩论。",
     ["第四次人机大战：王昱珩 vs 小度机器人", "人类观察力的天花板在哪里？", "AI能'看见'但能'看懂'吗？直觉是什么？", "人机共生的未来：水哥模式与AI时代的互补"],
     ["你认为在'观察力'这个维度上，人类还能胜过AI吗？如果会，在哪些方面？",
      "水哥的直觉式观察和AI的数据式识别有什么本质区别？",
      "如果你的工作被AI替代了一半，你保留下来的那部分会是什么？"]),
    (9, "水哥的生存法则——自由职业者的经济独立", "清华美院毕业后，水哥选择了自由职业。他没有进大厂，没有考公务员，甚至不怎么看微信。但他活得很好——有自己的设计工作室、景观设计项目、综艺出场费。他是如何做到的？",
     ["为什么拒绝体制：'我不喜欢跟人打交道'的自由选择", "自由职业者的经济学：技能垄断＞职位晋升", "水哥的收入结构拆解：设计、综艺、IP授权", "给想成为'数字游民'的你的三堂课"],
     ["如果你明天辞职，你的技能能在市场上独立变现吗？列出你的三项可市场化技能。",
      "水哥说他不喜欢跟人打交道——你觉得这是弱点还是优势？在什么场景下这是优势？",
      "设计一个'自由职业可行性评估'：你现在的积蓄能支撑多久？你的客户从哪里来？"]),
    (10, "独行者的世界观——水哥哲学体系总结", "从'微观辨水'到'我根本不需要朋友'，从清华怪才到全民偶像，水哥的人生看似反常规，却暗合一种极为自洽的哲学体系。这一课，我们将总结水哥的十大人生态度，并绘制一幅'独行者地图'。",
     ["水哥的十条人生准则：从独处到自由", "反脆弱性：右眼随时失明的男人为什么不怕", "独行者的社会价值：为什么世界需要异类", "致每一个'不合群'的你：你的时代来了"],
     ["从10课的学习中，选出对你最有冲击力的一个观点，写500字反思。",
      "如果你必须用一句话总结水哥的人生哲学，你会说什么？",
      "制定你的'独行者行动计划'：接下来的30天里，你会做出什么改变？"]),
]

def call_deepseek(prompt, max_tokens=2000):
    data = json.dumps({
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是康波研究院的课程撰写专家。请用流畅优美的中文撰写课程内容，风格参考《圆桌派》式的深度对话。每段200-400字，包含具体案例。使用HTML标签<p>和<blockquote>。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8, "max_tokens": max_tokens
    }).encode()
    req = urllib.request.Request(API_URL, data=data, headers={
        "Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"
    })
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read())["choices"][0]["message"]["content"]

def build_page(num, title, subtitle, sections, exercises):
    prev_num = num - 1 if num > 1 else None
    next_num = num + 1 if num < 10 else None
    prev_html = f'<a href="lesson{prev_num}.html">← 上一课</a>' if prev_num else '<span></span>'
    next_html = f'<a href="lesson{next_num}.html">下一课 →</a>' if next_num else '<span></span>'
    
    sections_html = ""
    for i, sec_title in enumerate(sections):
        prompt = f"""请为课程《{title}》撰写第{i+1}节内容（600-800字中文）。
本节标题：{sec_title}
要求：1个具体案例，1句<blockquote>引用，至少1处<strong>关键观点加粗</strong>。
风格：窦文涛《圆桌派》式的深度聊天质感。直接输出HTML段落。"""
        try:
            content = call_deepseek(prompt)
            sections_html += f'<h2>{sec_title}</h2>\n{content}\n'
            time.sleep(1)
        except Exception as e:
            sections_html += f'<h2>{sec_title}</h2>\n<p>生成中...（{e}）</p>\n'
    
    ex_html = '<div class="exercise"><h3>💡 思考练习</h3><ol>'
    for ex in exercises:
        ex_html += f'<li>{ex}</li>'
    ex_html += '</ol></div>'
    
    kc_html = f"""<h2>🔗 康波关联</h2>
<p>本课所讲的'{title}'主题与康波周期深度关联：在第六轮康波（2025-2035）的回升初期，<strong>个体独特性将成为最稀缺的资本</strong>。水哥式的非标人才——不依赖组织、不迎合主流、却有不可替代的核心能力——恰恰是康波春初最需要的物种。</p>"""
    
    return f"""<!DOCTYPE html>
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

base = "/root/shuige-course"
os.makedirs(base, exist_ok=True)

for num, title, subtitle, sections, exercises in COURSES_4_10:
    fpath = os.path.join(base, f"lesson{num}.html")
    if os.path.exists(fpath):
        print(f"lesson{num}.html exists, skip")
        continue
    print(f"Generating lesson{num}: {title}...")
    html = build_page(num, title, subtitle, sections, exercises)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  -> {len(html)} chars")
    time.sleep(1)

print("Done with courses 4-10")
