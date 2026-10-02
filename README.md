# Layer Finder

**Layer Finder** is a lightweight QGIS plugin for quickly finding and selecting layers and groups in the current project.

It is designed to make navigation easier in QGIS projects containing many layers, allowing you to find an item simply by typing part of its name.

## Features

* Search layers and groups by name
* Partial name matching
* Case-insensitive search
* Real-time search results while typing
* Navigate results with the **Up** and **Down** arrow keys
* Select the current result with **Enter**
* Select a result with a double click
* Select layers directly in the QGIS Layer Panel
* Supports nested groups
* Works with different QGIS layer types
* Simple and non-invasive interface
* No external dependencies

## Installation

Layer Finder can be installed through the standard QGIS plugin manager.

1. Open **QGIS**.
2. Open **Plugins → Manage and Install Plugins…**.
3. Search for **Layer Finder**.
4. Select the plugin and click **Install Plugin**.
5. Once installed, make sure **Layer Finder** is enabled.

After installation, the **Layer Finder** button will be available in the QGIS plugin toolbar.

## Usage

Click the **Layer Finder** button to open the search window.

Start typing the name of a layer or group. The results are updated automatically as you type.

Use:

* **↑ / ↓** to navigate through the results
* **Enter** to select the current result
* **Double click** to select a result

When a layer is selected, it becomes the current layer in the QGIS Layer Panel.

When a group is selected, the corresponding group is selected in the Layer Tree.

## Requirements

* QGIS **3.28 or later**
* Compatible with QGIS versions up to **4.99**

```

## Development

Layer Finder is developed in **Python**, using:

* **PyQGIS** for interaction with QGIS
* **PyQt** for the user interface

The plugin has no external Python dependencies and aims to keep the implementation simple, lightweight and easy to maintain.

## Current version

**0.1.8**

The current version focuses exclusively on fast, name-based searching and selection of layers and groups in the QGIS Layer Tree.

## Author

**Paolo Brunello**

Website: http://webstorymap.it/

## License

GPL 2.0 o successive



