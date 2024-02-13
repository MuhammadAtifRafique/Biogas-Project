# Biogas Project

## Overview

The Biogas Project is a web application designed to analyze blood samples and provide insights into potential health issues. The system measures various blood parameters using a combination of hardware and software components, including Raspberry Pi B+, PCA9548 I²C multiplexer, AS7262 color sensors, and a MySQL database for storing and retrieving data.

## Hardware Components

- **Raspberry Pi B+**: The central processing unit for the project, handling communication between the sensors and the server.
- **PCA9548 I²C Multiplexer**: Controls multiple AS7262 color sensors to detect blood colors.
- **AS7262 Color Sensors**: Detects specific wavelengths to measure the presence of various colors in the blood.
- **Mag Board (MCP4561T)**: Controls the brightness of LEDs for better blood cell visibility.
- **Linear Stepper Motor (DRV8843)**: Automates the opening and closing of the cylinder rack for blood sample insertion.

## Software Architecture

- **Backend**: Built with Flask, a Python micro web framework.
- **Database**: Uses MySQL for persistent storage of data.
- **Communication Protocol**: Employs MQTT for real-time communication between devices.

## API Endpoints

The following API endpoints are available:

- `/api/get_post_notes`: Retrieves post notes associated with a specific CSV file ID.
- `/api/post_post_notes`: Updates post notes for a specific CSV file ID.
- `/api/get_pre_notes`: Retrieves pre notes associated with a specific CSV file ID.
- `/api/post_pre_notes`: Updates pre notes for a specific CSV file ID.
- `/api/save_csv_meta_data`: Saves CSV metadata.
- `/api/add_group`: Adds a new group to the database.
- `/api/save_fav_setting`: Saves favorite settings for a group.
- `/api/check_login`: Checks login credentials.
- `/api/get_list_of_fav_settings`: Retrieves a list of favorite settings for a group.
- `/api/get_list_of_group`: Retrieves a list of groups.
- `/api/get_graph_meta_data`: Retrieves graph metadata for a specific CSV file ID.
- `/api/get_list_of_csv`: Retrieves a list of CSV files.
- `/api/get_grid_meta_data`: Retrieves grid metadata for a specific CSV file ID.
- `/api/rack-status`: Provides the status of the rack system.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or report any issues you encounter.

## License

This project is licensed under the terms of the MIT license.

---

©  2024 Muhammad Atif Rafique