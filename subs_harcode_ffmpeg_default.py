import os
import subprocess
import time
from glob import glob

def find_matching_vtt(mp4_file):
    base_name = os.path.splitext(mp4_file)[0]
    possible_vtt = glob(f"{base_name}.*.vtt") + glob(f"{base_name}.vtt")
    return possible_vtt[0] if possible_vtt else None

def safe_replace(src, dst, max_retries=5, delay=1):
    for i in range(max_retries):
        try:
            os.replace(src, dst)
            return True
        except PermissionError:
            if i < max_retries - 1:
                time.sleep(delay)
    return False

def safe_remove(file_path, max_retries=5, delay=1):
    for i in range(max_retries):
        try:
            os.remove(file_path)
            return True
        except PermissionError:
            if i < max_retries - 1:
                time.sleep(delay)
    return False

def burn_and_clean():
    print("=== MP4 + VTT Hardcode (GPU NVENC) ===")
    print("Burning subtitles and deleting originals...\n")

    for mp4 in glob("*.mp4"):
        vtt = find_matching_vtt(mp4)

        if not vtt or not os.path.exists(vtt):
            print(f"⚠️ No matching .vtt found for: {mp4}\n")
            continue

        temp_output = f"temp_{mp4}"
        vtt_path = vtt.replace("\\", "/")  # IMPORTANT for Windows

        print(f"🔥 Burning: {mp4} + {vtt}")

        try:
            subprocess.run([
                "ffmpeg",
                "-hwaccel", "cuda",
                "-i", mp4,
                "-vf", f"subtitles='{vtt_path}'",
                "-c:v", "h264_nvenc",
                "-preset", "p5",        # p6 = faster, p4 = higher quality
                "-cq", "18",
                "-c:a", "copy",
                temp_output
            ], check=True)

            if os.path.exists(temp_output):
                if safe_replace(temp_output, mp4):
                    if safe_remove(vtt):
                        print(f"✅ Success! Burned & deleted: {vtt}\n")
                    else:
                        print(f"⚠️ Warning: Could not delete {vtt}\n")
                else:
                    print("❌ Error: Could not replace original MP4\n")
            else:
                print("❌ Error: Temp output not created\n")

        except subprocess.CalledProcessError:
            if os.path.exists(temp_output):
                safe_remove(temp_output)
            print("❌ FFmpeg processing failed\n")

if __name__ == "__main__":
    burn_and_clean()
    input("Press Enter to exit...")
