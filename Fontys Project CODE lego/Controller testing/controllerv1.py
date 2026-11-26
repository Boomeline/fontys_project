"""
LEGO Double Motor controller (alleen Windows)

Bediening (houd de toets ingedrukt):
    A      = linkermotor draait (70%)
    D      = rechtermotor draait (70%)
    A + D  = beide motoren draaien tegelijk
    S      = boost: beide motoren 4 seconden op 100%, daarna terug naar normaal
    Q      = veilig stoppen en verbinding verbreken

Gebruikte functies uit de officiele LEGO Education Python API:
    DoubleMotor(), connect(), connected, disconnect()
    movement_move_tank(speed_left, speed_right, blocking=...)
    movement_stop(), motor_stop(motor=le.MOTOR_BOTH)
"""

import ctypes
import msvcrt
import time

import legoeducation as le

# ---------------------------------------------------------------
# INSTELLINGEN - hier pas je dingen aan
# ---------------------------------------------------------------
CARD_COLOR = le.LEGO_COLOR_GREEN
CARD_SERIAL = "1857"

NORMAL_SPEED = 60       # normale snelheid in procenten (0-100)
BOOST_SPEED = 40       # boostsnelheid in procenten (0-100)
BOOST_SECONDS = 2.0     # hoe lang de boost duurt
POLL_INTERVAL = 0.02    # hoe vaak we de toetsen controleren (20 ms = 50x per seconde)

# Draait een motor de verkeerde kant op? Zet de waarde dan op -1.
LEFT_DIRECTION = 1
RIGHT_DIRECTION = 1

# Windows "virtual key codes" voor de toetsen
VK_A = 0x41
VK_D = 0x44
VK_S = 0x53
VK_Q = 0x51

# ---------------------------------------------------------------
# TOETSEN LEZEN
# ---------------------------------------------------------------
# msvcrt.getwch() meldt alleen dat een toets is INGEDRUKT (en daarna de
# herhaalde tekens van Windows). Loslaten en meerdere toetsen tegelijk
# kan het niet zien. GetAsyncKeyState vraagt wel aan Windows: "is deze
# toets op dit moment ingedrukt?" - voor elke toets apart.
_user32 = ctypes.windll.user32
_user32.GetAsyncKeyState.argtypes = [ctypes.c_int]
_user32.GetAsyncKeyState.restype = ctypes.c_short


def key_is_down(vk_code):
    """True zolang de toets fysiek ingedrukt is."""
    return (_user32.GetAsyncKeyState(vk_code) & 0x8000) != 0


def clear_keyboard_buffer():
    """Gooi getypte tekens weg, zodat ze niet in je terminal blijven staan.
    Hier gebruiken we msvcrt nog wel voor."""
    while msvcrt.kbhit():
        msvcrt.getwch()


# ---------------------------------------------------------------
# MOTOREN AANSTUREN
# ---------------------------------------------------------------
def clamp_percent(value):
    """Houd de snelheid binnen -100 en 100."""
    return max(-100, min(100, int(value)))


def send_speeds(doublemotor, left, right):
    """Stuur links en rechts in EEN commando, zodat ze tegelijk starten."""
    if left == 0 and right == 0:
        doublemotor.movement_stop()
    else:
        doublemotor.movement_move_tank(
            clamp_percent(left) * LEFT_DIRECTION,
            clamp_percent(right) * RIGHT_DIRECTION,
            blocking=False,  # wacht niet op de motor, de loop blijft doorlopen
        )


def stop_all(doublemotor):
    """Stop alles. Elke stap staat in een eigen try, zodat een fout in
    de ene stap de andere niet overslaat."""
    for action in (
        lambda: doublemotor.movement_stop(),
        lambda: doublemotor.motor_stop(motor=le.MOTOR_BOTH),
    ):
        try:
            action()
        except Exception as error:
            print(f"Waarschuwing bij stoppen: {error}")


# ---------------------------------------------------------------
# HOOFDPROGRAMMA
# ---------------------------------------------------------------
def main():
    doublemotor = le.DoubleMotor()

    try:
        doublemotor.connect(card_color=CARD_COLOR, card_serial=CARD_SERIAL)
    except Exception as error:
        print(f"Error connecting to Double Motor: {error}")
        return 1

    if not doublemotor.connected:
        print("Error connecting to Double Motor.")
        return 1

    print("LEGO Double Motor connected!")
    print(f"A = linkermotor ({NORMAL_SPEED}%)   D = rechtermotor ({NORMAL_SPEED}%)")
    print(f"S = boost ({BOOST_SPEED}% gedurende {BOOST_SECONDS:g} s)   Q = stoppen")
    print("Let op: toetsen werken ook als dit venster niet actief is.")

    boost_until = 0.0        # tijdstip waarop de boost eindigt
    s_was_down = False       # om alleen het INDRUKKEN van S op te merken
    last_speeds = None       # laatst verstuurde (links, rechts)
    was_boosting = False

    try:
        while True:
            if not doublemotor.connected:
                print("Verbinding verloren.")
                break

            if key_is_down(VK_Q):
                print("Shutting down...")
                break

            now = time.monotonic()

            # --- Boost starten bij het indrukken van S ---
            s_is_down = key_is_down(VK_S)
            boosting = now < boost_until
            if s_is_down and not s_was_down and not boosting:
                boost_until = now + BOOST_SECONDS
                boosting = True
                print(f"BOOST! {BOOST_SECONDS:g} seconden")
            s_was_down = s_is_down

            if was_boosting and not boosting:
                print("Boost voorbij, terug naar normale snelheid.")
            was_boosting = boosting

            # --- Gewenste snelheden bepalen ---
            if boosting:
                left = BOOST_SPEED
                right = BOOST_SPEED
            else:
                left = NORMAL_SPEED if key_is_down(VK_A) else 0
                right = NORMAL_SPEED if key_is_down(VK_D) else 0

            # --- Alleen een commando sturen als er iets verandert ---
            if (left, right) != last_speeds:
                send_speeds(doublemotor, left, right)
                last_speeds = (left, right)

            clear_keyboard_buffer()
            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\nOnderbroken met Ctrl+C.")
    except Exception as error:
        print(f"Fout tijdens het rijden: {error}")
    finally:
        # Dit blok draait ALTIJD, ook bij een crash.
        stop_all(doublemotor)
        try:
            doublemotor.disconnect()
        except Exception as error:
            print(f"Waarschuwing bij verbreken: {error}")
        print("Disconnected. Goodbye!")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())