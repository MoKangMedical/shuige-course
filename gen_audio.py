#!/usr/bin/env python3
"""Moss-TTS-Nano audio generation for shuige courses - run from MOSS-TTS-Nano dir"""
import sys, os, subprocess, time

# Ensure we can import onnx_tts_runtime from the repo dir
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from onnx_tts_runtime import OnnxTtsRuntime

SCRIPTS = {
    1: "欢迎来到水哥课程第一课：微观辨水，超强观察力的养成。从520杯水中辨出指定的一杯，王昱珩用近乎神迹的表现征服了全中国。",
    2: "第二课：清华往事，天才不需要合群。高考专业第一、自闭症经历，水哥证明了天才的成长不需要合群。",
    3: "第三课：我不需要朋友，独处的力量。水哥在圆桌派上直言不需要朋友，他对独处的理解是当代人最稀缺的智慧。",
    4: "第四课：婚姻的真相，两个独立个体的契约。水哥直言和妻子的关系全是假的，他不是在否定婚姻，而是在重新定义婚姻。",
    5: "第五课：自闭症到鬼才之眼，神经多样性的礼物。高功能自闭症如何转化为超能力？重新定义正常，世界需要不同的大脑。",
    6: "第六课：用眼睛破案，观察力如何改变现实。水哥凭监控视频协助警方破获肇事逃逸案，观察力的现实应用远比综艺更有意义。",
    7: "第七课：植物的智慧，从养动植物中学习生命。水哥的家是一个植物园，他说植物教会他的东西比任何人都多。",
    8: "第八课：人机大战，当最强人类大脑遇到人工智能。2017年王昱珩对战小度机器人，一场关于智慧本质的哲学辩论。",
    9: "第九课：水哥的生存法则，自由职业者的经济独立。拒绝体制、不看微信，水哥如何在保持独立的同时实现经济自由。",
    10: "第十课：独行者的世界观，水哥哲学体系总结。十条人生准则、反脆弱性，绘制一幅完整的独行者地图。",
}

AUDIO_DIR = "/var/www/kangboacademy/frontend/shuige/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

print("Initializing Moss-TTS-Nano...", flush=True)
rt = OnnxTtsRuntime()
print("Ready!", flush=True)

for num in range(1, 11):
    text = SCRIPTS[num]
    mp3_path = f"{AUDIO_DIR}/lesson{num}.mp3"
    if os.path.exists(mp3_path) and os.path.getsize(mp3_path) > 1000:
        print(f"lesson{num}.mp3 exists ({os.path.getsize(mp3_path)} bytes), skip", flush=True)
        continue
    
    wav_path = f"/home/ubuntu/shuige_{num}.wav"
    print(f"Lesson {num} ({len(text)} chars)...", flush=True)
    
    try:
        result = rt.synthesize(text=text, voice="Junhao", output_audio_path=wav_path)
        dur = result.get("duration", 0)
        print(f"  WAV {dur:.1f}s, converting...", flush=True)
        
        subprocess.run([
            "ffmpeg", "-y", "-i", wav_path,
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=9",
            "-ar", "24000", "-ac", "1", "-b:a", "48k", mp3_path
        ], capture_output=True)
        os.remove(wav_path)
        print(f"  OK ({os.path.getsize(mp3_path)} bytes)", flush=True)
    except Exception as e:
        print(f"  ERROR: {e}", flush=True)

print("\nDone! Files:", flush=True)
for num in range(1, 11):
    mp3_path = f"{AUDIO_DIR}/lesson{num}.mp3"
    s = os.path.getsize(mp3_path) if os.path.exists(mp3_path) else 0
    print(f"  lesson{num}.mp3: {s} bytes", flush=True)
