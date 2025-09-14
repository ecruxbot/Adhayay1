# SD_Card_data

This directory contains all shared resources essential for the operation of Adhyay-1 robotics kit projects, especially when using CircuitPython and Raspberry Pi Pico W.

## Purpose

SD_Card_data serves as a centralized storage location for libraries, media files, and supporting assets required by various examples and kit functionalities.

## Contents

- **lib/**  
  Custom libraries for hardware modules, including sensor drivers, display control, and communication routines.

- **fonts/**  
  Font files for the OLED display, used to render text and graphical information.

- **animation/**  
  Graphic files and animations for OLED display demos and visual feedback.

- **sounds/**  
  Audio files including tones, melodies, and sound effects for playback through the onboard speaker.



## Usage

For CircuitPython projects on PicoW:
- Mount the SD card at startup using the provided library initialization commands.
- Import required libraries from /sd/lib/ in your scripts.
- Reference font and graphic files for rich display output.
- Play audio resources for interactive feedback in robotics projects.

Refer to getting started guides and library documentation for correct usage and mounting procedures.
