#!/usr/bin/env python3
"""
Klipper API Interaction Script
Demonstrates how to interact with Klipper through the Moonraker API
"""

import requests
import json
import time
from typing import Dict, Any, Optional
from termcolor import colored


def niceprint(text):
    print((colored(text, 'green')))


def badprint(text):
    print((colored(text, 'red')))


class MoonrakerConnector:
    def __init__(self, host: str = "localhost", port: int = 7125):
        """
        Initialize Klipper API connection

        Args:
            host: Moonraker host address (default: localhost)
            port: Moonraker port (default: 7125)
        """
        self.base_url = f"http://{host}:{port}"
        self.verify_connection()

    def verify_connection(self):
        """Verify connection to Moonraker API"""
        try:
            response = requests.get(f"{self.base_url}/server/info", timeout=5)
            response.raise_for_status()
            niceprint(f"Connected to Klipper/Moonraker at {self.base_url}")
        except requests.exceptions.RequestException as e:
            badprint(f"Failed to connect to Moonraker at {self.base_url}")
            badprint(f"  Error: {e}")
            badprint("  Make sure Moonraker is running and accessible")
            raise

    def get_motion_report(self) -> Dict[str, float]:
        """
        Get "motion report"
        """
        try:
            response = requests.get(
                f"{self.base_url}/printer/objects/query",
                params="motion_report"
            )
            response.raise_for_status()
            data = response.json()
            motion_report = data.get("result", {}).get("status", {}).get("motion_report", {})
            return motion_report

        except requests.exceptions.RequestException as e:
            print(f"Error getting motion report: {e}")
            return {}

    def execute_gcode(self, gcode: str) -> bool:
        """
        Execute G-code command

        Args:
            gcode: G-code command to execute

        Returns:
            True if successful, False otherwise
        """
        try:
            response = requests.post(
                f"{self.base_url}/printer/gcode/script",
                json={"script": gcode}
            )
            response.raise_for_status()
            return True

        except requests.exceptions.RequestException as e:
            badprint(f"Error executing G-code: {e}")
            return False

    def home_axes(self, axes: str = "XYZ") -> bool:
        """
        Home specified axes

        Args:
            axes: Axes to home (e.g., "XYZ", "XY", "Z")

        Returns:
            True if successful, False otherwise
        """
        gcode = f"G28 {' '.join(axes)}"
        print(f"Homing axes: {axes}")
        return self.execute_gcode(gcode)

    def move_toolhead(
        self,
        x: Optional[float] = None,
        y: Optional[float] = None,
        z: Optional[float] = None,
        feedrate: int = 3000
    ) -> bool:
        """
        Move toolhead to specified position

        Args:
            x: X position (None to keep current)
            y: Y position (None to keep current)
            z: Z position (None to keep current)
            feedrate: Movement speed in mm/min

        Returns:
            True if successful, False otherwise
        """
        # Build G-code command
        gcode = f"G1 F{feedrate}"
        if x is not None:
            gcode += f" X{x}"
        if y is not None:
            gcode += f" Y{y}"
        if z is not None:
            gcode += f" Z{z}"

        print(f"Moving toolhead with: {gcode}")
        return self.execute_gcode(gcode)

    def emergency_stop(self) -> bool:
        """
        Trigger emergency stop

        Returns:
            True if successful, False otherwise
        """
        try:
            response = requests.post(f"{self.base_url}/printer/emergency_stop")
            response.raise_for_status()
            niceprint("Emergency stop triggered!")
            return True

        except requests.exceptions.RequestException as e:
            badprint(f"Error triggering emergency stop: {e}")
            return False

    def get_system_info(self) -> Dict[str, Any]:
        """
        Get system information

        Returns:
            Dictionary with system information
        """
        try:
            response = requests.get(f"{self.base_url}/machine/system_info")
            response.raise_for_status()
            return response.json().get("result", {}).get("system_info", {})

        except requests.exceptions.RequestException as e:
            badprint(f"Error getting system info: {e}")
            return {}


def main():
    print("Klipper API Interaction Demo")
    print("=" * 50)

    try:
        # Connect to Klipper
        klipper = MoonrakerConnector(host="localhost", port=7125)

        # Get and display motion report
        print("\nCurrent Toolhead motion report:")
        motion_report = klipper.get_motion_report()
        if motion_report:
            print(f'Live position: {motion_report['live_position']}')
            print(f'Live velocity: {motion_report['live_velocity']}')
            print(f'Live extruder velocity: {motion_report['live_extruder_velocity']}')
            print(f'Steppers: {motion_report['steppers']}')

        # Set absolute positioning
        if klipper.execute_gcode("G90"):
            niceprint("Set absolute positioning (G90)")

        # You can uncomment these to test movement (be careful!)
        klipper.home_axes("XY")  # Home X and Y axes
        time.sleep(2)
        klipper.move_toolhead(x=100, y=100, feedrate=6000)  # Move to X100 Y100

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Klipper and Moonraker are running")
        print("2. Check that Moonraker is accessible on port 7125")
        print("3. Verify your printer is connected and powered on")
        print("4. Check Moonraker configuration allows API access")


if __name__ == "__main__":
    main()