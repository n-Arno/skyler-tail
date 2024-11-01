#!/usr/bin/env python3

import sys, os
import subprocess
from PIL import Image, ImageFont, ImageDraw
from time import sleep

WIDTH = 800
HEIGHT = 600
LINES = 35
FONTSIZE = 16
FONTNAME = "./MonaspaceNeon-Regular.otf"
SKYLER = "./skyler.png"


def usage():
    print(f"{sys.argv[0]} logfile.txt image.png")
    sys.exit(1)


def tail(f, l):
    cmd = f"tail -n {l} {f}".split(" ")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = proc.communicate()
    if err:
        raise Exception(err.decode())

    return "\n".join(output.decode().split("\n")[::-1]).strip()


def pos(i1, i2):
    s1 = i1.size
    s2 = i2.size
    return (s1[0] - s2[0], s1[1] - s2[1])


def main():
    if len(sys.argv) != 3:
        usage()

    filename = sys.argv[1]
    imgname = sys.argv[2]

    font = ImageFont.truetype(FONTNAME, size=FONTSIZE)
    skyler = Image.open(SKYLER)
    img = Image.new("RGBA", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)

    print(f"Tailing {filename} to {imgname}\nCtrl-C to exit")

    try:
        while True:
            sleep(1)
            if not os.path.exists(filename):
                continue

            loglines = tail(filename, LINES)
            draw.rectangle([(0, 0), img.size], fill=(0, 0, 0, 255))
            draw.multiline_text((0, 0), loglines, font=font, fill=(255, 255, 255, 255))
            img.paste(skyler, pos(img, skyler), skyler)
            img.save(imgname)
    except KeyboardInterrupt:
        print("\nExiting!")
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
