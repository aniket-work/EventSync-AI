from PIL import Image, ImageDraw, ImageFont
import time
import os

# Configuration
WIDTH, HEIGHT = 900, 600
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (240, 240, 240)
HEADER_COLOR = (50, 50, 50)
PROMPT_COLOR = (100, 255, 100)
COMMAND_COLOR = (255, 255, 100)
CURSOR_COLOR = (200, 200, 200)

def create_terminal_base():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    # Window controls
    draw.ellipse([15, 15, 30, 30], fill=(255, 95, 87)) # Red
    draw.ellipse([40, 15, 55, 30], fill=(255, 189, 46)) # Yellow
    draw.ellipse([65, 15, 80, 30], fill=(39, 201, 63)) # Green
    draw.rectangle([0, 0, WIDTH, 45], outline=HEADER_COLOR, width=1)
    return img

def generate_gif():
    frames = []
    base = create_terminal_base()
    draw = ImageDraw.Draw(base)
    
    # Try to load a monospaced font
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New.ttf", 18)
    except:
        font = ImageFont.load_default()

    current_text = "$ python main.py"
    x, y = 20, 70
    
    # Typing effect
    for i in range(len(current_text) + 1):
        frame = base.copy()
        f_draw = ImageDraw.Draw(frame)
        f_draw.text((x, y), current_text[:i], font=font, fill=TEXT_COLOR)
        if i < len(current_text) or (time.time() * 2) % 2 == 0:
            f_draw.rectangle([x + f_draw.textlength(current_text[:i], font=font), y, x + f_draw.textlength(current_text[:i], font=font) + 10, y + 20], fill=CURSOR_COLOR)
        frames.extend([frame] * 3)
    
    # Execution logs
    logs = [
        "",
        "=== EventSync-AI: Corporate Event Logistics Orchestrator ===",
        "System: Initializing multi-agent workflow...",
        "[PROCESS] Planner Node: Designing event architecture...",
        "Selected Grand Plaza Hotel and Elite Gourmet.",
        "Budget calculated: $20000. Approval required: True",
        "Waiting for human approval... (Simulated)",
        "### EVENT FINALIZATION REPORT",
        "- Venue: Grand Plaza Hotel (ID: EVT-84291)",
        "- Catering: Elite Gourmet (ID: EVT-19420)",
        "=== Simulation Complete ==="
    ]
    
    current_y = y + 30
    for line in logs:
        frame = frames[-1].copy()
        f_draw = ImageDraw.Draw(frame)
        f_draw.text((x, current_y), line, font=font, fill=TEXT_COLOR)
        frames.extend([frame] * 5)
        current_y += 25

    # Simple UI representation frame
    ui_frame = Image.new("RGB", (WIDTH, HEIGHT), (245, 247, 250))
    ui_draw = ImageDraw.Draw(ui_frame)
    ui_draw.rectangle([20, 20, WIDTH-20, 80], fill=(255, 255, 255), outline=(200, 200, 200))
    ui_draw.text((40, 35), "EventSync-AI Dashboard", fill=(50, 50, 50), font=font)
    ui_draw.rectangle([40, 100, 400, 300], fill=(255, 255, 255), outline=(200, 200, 200))
    ui_draw.text((60, 120), "Total Cost: $20,000", fill=(255, 95, 87), font=font)
    ui_draw.text((60, 160), "Status: WAITING FOR APPROVAL", fill=(255, 189, 46), font=font)
    frames.extend([ui_frame] * 40)

    # Palette optimization strategy as per rules
    sample = Image.new("RGB", (WIDTH, HEIGHT * 3))
    sample.paste(frames[0], (0,0))
    sample.paste(frames[len(frames)//2], (0, HEIGHT))
    sample.paste(frames[-1], (0, HEIGHT*2))
    palette = sample.quantize(colors=256, method=2)

    final_frames = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
    os.makedirs("images", exist_ok=True)
    final_frames[0].save("images/title-animation.gif", save_all=True, append_images=final_frames[1:], optimize=True, loop=0, duration=100)
    print("Successfully generated images/title-animation.gif")

if __name__ == "__main__":
    generate_gif()
