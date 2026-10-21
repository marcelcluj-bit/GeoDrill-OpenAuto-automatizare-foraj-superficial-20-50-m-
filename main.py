"""
GeoDrill-OpenAuto: Real-Time Shallow Drilling Telemetry & Control Unit
License: MIT / Public Domain CC0
Hardware Target: Raspberry Pi 4 / ESP32 Microcontroller Platform
"""

import time
import json
import random  # Simulated sensor telemetry for hardware validation

class DrillingTelemetrySystem:
    def __init__(self, target_depth_m=50.0):
        self.target_depth_m = target_depth_m
        self.current_depth_m = 0.0
        self.rpm = 0
        self.torque_nm = 0.0
        self.wob_kg = 0.0  # Weight on Bit
        self.mud_pressure_psi = 0.0
        self.emergency_stop = False

    def read_sensors(self):
        """Simulate reading data from Hall effect RPM sensor, load cells, and pressure transducers."""
        self.rpm = random.randint(120, 250)
        self.torque_nm = round(random.uniform(45.0, 120.0), 2)
        self.wob_kg = round(random.uniform(150.0, 400.0), 1)
        self.mud_pressure_psi = round(random.uniform(15.0, 45.0), 1)

    def evaluate_safety_thresholds(self):
        """Automated logic to prevent pipe jamming or over-pressurization."""
        if self.torque_nm > 110.0:
            print("[WARN] High Torque Detected! Reducing ROP and adjusting Weight-on-Bit.")
            self.wob_kg -= 50.0
        if self.mud_pressure_psi > 40.0:
            print("[CRITICAL] High Mud Pressure! Potential borehole clogging.")
            
    def step_drilling_cycle(self, rop_m_per_hr=2.5):
        """Simulate 1-minute drilling increment."""
        if self.emergency_stop or self.current_depth_m >= self.target_depth_m:
            return False

        self.read_sensors()
        self.evaluate_safety_thresholds()
        
        # Advance depth (depth per second at current ROP)
        depth_increment = (rop_m_per_hr / 3600.0) * 10
        self.current_depth_m = min(self.target_depth_m, self.current_depth_m + depth_increment)
        
        telemetry_payload = {
            "timestamp": time.time(),
            "depth_m": round(self.current_depth_m, 3),
            "rpm": self.rpm,
            "torque_nm": self.torque_nm,
            "wob_kg": self.wob_kg,
            "mud_pressure_psi": self.mud_pressure_psi
        }
        
        print(f"[TELEMETRY] Depth: {telemetry_payload['depth_m']}m / {self.target_depth_m}m | Torque: {telemetry_payload['torque_nm']}Nm | RPM: {telemetry_payload['rpm']}")
        return True

if __name__ == "__main__":
    print("Initializing GeoDrill-OpenAuto Controller...")
    rig = DrillingTelemetrySystem(target_depth_m=35.0)
    
    for _ in range(10):
        if not rig.step_drilling_cycle():
            break
        time.sleep(0.5)
