import threading
import tkinter as tk
from tkinter import ttk

import legoeducation as le

COLORS = ["GREEN", "BLUE", "RED", "ORANGE", "YELLOW", "AZURE", "PURPLE", "MAGENTA"]


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LEGO Double Motor")
        self.geometry("420x360")
        self.resizable(False, False)

        self.doublemotor = None
        self.position_job = None
        self.busy = False  # voorkomt dat motorcommando's door elkaar lopen

        self.setup_frame = tk.Frame(self, padx=30, pady=25)
        self.control_frame = tk.Frame(self)

        self.build_setup()
        self.build_control()

        self.setup_frame.pack(fill="both", expand=True)
        self.protocol("WM_DELETE_WINDOW", self.quit_app)

    # ---------- Verbindingsscherm ----------
    def build_setup(self):
        f = self.setup_frame

        tk.Label(f, text="Verbind met Double Motor", font=("Segoe UI", 15, "bold")).pack(pady=(0, 15))

        tk.Label(f, text="Welke kleur kaart heb je?", anchor="w").pack(fill="x")
        self.color_var = tk.StringVar(value=COLORS[0])
        self.color_box = ttk.Combobox(f, textvariable=self.color_var, values=COLORS, state="readonly")
        self.color_box.pack(fill="x", pady=(2, 12))

        tk.Label(f, text="Vul de code in (4 cijfers, bijv. 1857):", anchor="w").pack(fill="x")
        self.serial_var = tk.StringVar()
        self.serial_var.trace_add("write", lambda *_: self.update_continue_state())
        vcmd = (self.register(self.validate_serial), "%P")
        self.serial_entry = tk.Entry(f, textvariable=self.serial_var, validate="key", validatecommand=vcmd,
                                     font=("Segoe UI", 14), justify="center")
        self.serial_entry.pack(fill="x", pady=(2, 15))
        self.serial_entry.bind("<Return>", lambda _e: self.connect())

        self.continue_btn = tk.Button(f, text="Doorgaan", font=("Segoe UI", 12, "bold"),
                                      state="disabled", command=self.connect)
        self.continue_btn.pack(fill="x", ipady=6)

        self.status_label = tk.Label(f, text="", font=("Segoe UI", 10), wraplength=350)
        self.status_label.pack(pady=(12, 0))

    @staticmethod
    def validate_serial(new_value):
        return new_value == "" or (new_value.isdigit() and len(new_value) <= 4)

    def update_continue_state(self):
        ok = len(self.serial_var.get()) == 4 and not self.busy
        self.continue_btn.config(state="normal" if ok else "disabled")

    def set_status(self, text, color="black"):
        self.status_label.config(text=text, fg=color)

    def connect(self):
        if len(self.serial_var.get()) != 4 or self.busy:
            return
        self.busy = True
        self.color_box.config(state="disabled")
        self.serial_entry.config(state="disabled")
        self.continue_btn.config(state="disabled")
        self.set_status("Bezig met verbinden...", "#555555")

        color_name = self.color_var.get()
        serial = self.serial_var.get()
        threading.Thread(target=self._connect_worker, args=(color_name, serial), daemon=True).start()

    def _connect_worker(self, color_name, serial):
        try:
            card_color = getattr(le, f"LEGO_COLOR_{color_name}")
            motor = le.DoubleMotor()
            motor.connect(card_color=card_color, card_serial=serial)
            ok = motor.connected
        except Exception as e:  # noqa: BLE001
            self.after(0, self._connect_failed, f"Fout: {e}")
            return

        if ok:
            self.after(0, self._connect_success, motor)
        else:
            self.after(0, self._connect_failed, "Verbinding mislukt. Controleer kleur en code.")

    def _connect_failed(self, message):
        self.busy = False
        self.color_box.config(state="readonly")
        self.serial_entry.config(state="normal")
        self.update_continue_state()
        self.set_status(message, "red")

    def _connect_success(self, motor):
        self.doublemotor = motor
        self.busy = False
        self.set_status("Verbonden!", "green")
        self.after(400, self.show_control)

    # ---------- Controlpaneel ----------
    def build_control(self):
        f = self.control_frame

        tk.Button(f, text="Quit", font=("Segoe UI", 11, "bold"), bg="#d9534f", fg="white",
                  width=8, command=self.quit_app).place(x=10, y=10)

        self.left_btn = tk.Button(f, text="▲", font=("Segoe UI", 48), width=3, height=1,
                                  command=self.motor_left)
        self.left_btn.place(x=35, y=120)

        self.right_btn = tk.Button(f, text="▲", font=("Segoe UI", 48), width=3, height=1,
                                   command=self.motor_right)
        self.right_btn.place(x=235, y=120)

        tk.Label(f, text="Motor links", font=("Segoe UI", 10)).place(x=65, y=250)
        tk.Label(f, text="Motor rechts", font=("Segoe UI", 10)).place(x=262, y=250)

        self.left_pos_label = tk.Label(f, text="Positie: -", font=("Consolas", 12, "bold"))
        self.left_pos_label.place(x=45, y=290)
        self.right_pos_label = tk.Label(f, text="Positie: -", font=("Consolas", 12, "bold"))
        self.right_pos_label.place(x=245, y=290)

    def show_control(self):
        self.setup_frame.pack_forget()
        self.control_frame.pack(fill="both", expand=True)
        self.update_positions()

    def update_positions(self):
        """Leest elke 100 ms de positie van beide wielen uit en toont die."""
        if self.doublemotor is None:
            return
        try:
            left = self.doublemotor.motor[le.MOTOR_LEFT].position
            right = self.doublemotor.motor[le.MOTOR_RIGHT].position
            self.left_pos_label.config(text=f"Positie: {left}")
            self.right_pos_label.config(text=f"Positie: {right}")
            print(f"Left Position: {left}, Right Position: {right}")
        except Exception:  # noqa: BLE001
            pass
        self.position_job = self.after(100, self.update_positions)

    def _run_motor(self, degrees, motor):
        if self.busy or self.doublemotor is None:
            return
        self.busy = True

        def worker():
            try:
                self.doublemotor.motor_run_for_degrees(degrees, motor=motor)
            finally:
                self.busy = False

        threading.Thread(target=worker, daemon=True).start()

    def motor_left(self):
        self._run_motor(-90, le.MOTOR_LEFT)

    def motor_right(self):
        self._run_motor(90, le.MOTOR_RIGHT)

    # ---------- Afsluiten ----------
    def quit_app(self):
        if self.position_job is not None:
            self.after_cancel(self.position_job)
            self.position_job = None
        motor, self.doublemotor = self.doublemotor, None
        try:
            if motor is not None:
                motor.disconnect()
        except Exception:  # noqa: BLE001
            pass
        self.destroy()


if __name__ == "__main__":
    App().mainloop()