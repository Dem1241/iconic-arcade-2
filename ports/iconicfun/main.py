#!/usr/bin/env python3
"""Iconic Fun - step 1: control tester.

Proves pygame runs as a Batocera port and shows how the arcade
stick and buttons map (which button number is which).
Exit: ESC on a keyboard, or hold any 2 buttons for 2 seconds.
"""
import math

import pygame

BG = (10, 10, 14)
FG = (236, 236, 242)
DIM = (60, 60, 74)
ACCENT = (255, 64, 129)
EXIT_HOLD = 2.0  # seconds


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.mouse.set_visible(False)
    w, h = screen.get_size()
    clock = pygame.time.Clock()

    title_font = pygame.font.Font(None, h // 5)
    text_font = pygame.font.Font(None, h // 20)
    small_font = pygame.font.Font(None, h // 36)

    joysticks = {}
    held_since = None
    running = True

    while running:
        t = pygame.time.get_ticks() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
            elif event.type == pygame.JOYDEVICEREMOVED:
                joysticks.pop(event.instance_id, None)

        screen.fill(BG)

        # Title with a soft pulse
        pulse = 0.5 + 0.5 * math.sin(t * 2)
        title = title_font.render("ICONIC", True, lerp(FG, ACCENT, pulse))
        screen.blit(title, title.get_rect(center=(w // 2, h // 6)))

        if not joysticks:
            msg = text_font.render("no controller found", True, DIM)
            screen.blit(msg, msg.get_rect(center=(w // 2, h // 2)))

        pressed_total = 0
        row_h = h * 0.55 / max(len(joysticks), 1)

        for row, joy in enumerate(joysticks.values()):
            y = int(h * 0.33 + row_h * row + row_h / 2)
            r = int(min(row_h * 0.3, h * 0.08))
            cx = w // 10 + r

            label = text_font.render(f"P{row + 1}   {joy.get_name()}", True, DIM)
            screen.blit(label, (w // 10, y - r - label.get_height() - 10))

            # Stick: axes 0/1, or the d-pad hat if the encoder reports one
            ax = joy.get_axis(0) if joy.get_numaxes() > 0 else 0
            ay = joy.get_axis(1) if joy.get_numaxes() > 1 else 0
            if joy.get_numhats():
                hx, hy = joy.get_hat(0)
                ax, ay = ax or hx, ay or -hy
            pygame.draw.circle(screen, DIM, (cx, y), r, 3)
            dot = (int(cx + ax * r * 0.7), int(y + ay * r * 0.7))
            pygame.draw.circle(screen, ACCENT, dot, max(r // 4, 4))

            # Buttons, numbered so you can learn the mapping
            br = max(r // 3, 8)
            for b in range(joy.get_numbuttons()):
                bx = cx + r * 2 + b * br * 3
                on = joy.get_button(b)
                pressed_total += on
                pygame.draw.circle(screen, ACCENT if on else DIM, (bx, y), br, 0 if on else 2)
                num = small_font.render(str(b), True, FG if on else DIM)
                screen.blit(num, num.get_rect(center=(bx, y + br + 16)))

        # Hold 2+ buttons to exit, with a progress bar
        if pressed_total >= 2:
            if held_since is None:
                held_since = t
            progress = (t - held_since) / EXIT_HOLD
            pygame.draw.rect(screen, ACCENT, (0, h - 6, int(w * min(progress, 1)), 6))
            if progress >= 1:
                running = False
        else:
            held_since = None

        hint = small_font.render("hold any 2 buttons to exit", True, DIM)
        screen.blit(hint, hint.get_rect(midbottom=(w // 2, h - 24)))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
