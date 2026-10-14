import json, os, sys
os.environ["PATH"] = r"C:\Users\prosy\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin;" + os.environ["PATH"]
import whisper
m = whisper.load_model("small")
r = m.transcribe(sys.argv[1], language="pt", word_timestamps=True, fp16=False)
json.dump(r, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False)
for s in r["segments"]:
    print(f'{s["start"]:7.2f} {s["end"]:7.2f} {s["text"]}')
