# Status Kitchen Recipes

Community-contributed recipes for [Status Kitchen](https://github.com/keithvassallomt/statuskitchen), the GNOME Shell extension that turns tray icons into native top bar indicators.

## What is a Recipe?

A recipe is a configuration file that tells Status Kitchen how to transform a specific application's tray icon into a GNOME Shell indicator. Recipes define:

- Which application to target (via D-Bus name pattern)
- Icon configuration (static, dynamic, symbolic)
- Menu items to expose in the indicator

## Installing Recipes

### From the Web UI

1. Visit [statuskitchen.app](https://statuskitchen.app) (coming soon)
2. Browse available recipes
3. Click "Install" on the recipe you want
4. Status Kitchen will automatically download and install the recipe

### From Status Kitchen App

1. Open Status Kitchen
2. Click "Browse Cookbook" in the header bar
3. Find and install recipes directly from the app

### Manual Installation

1. Download the `.skr` file from the recipe's `dist/` folder
2. Open Status Kitchen
3. Use "Import Recipe" to load the file

## Contributing a Recipe

We welcome recipe contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed submission guidelines.

### Quick Start

1. Create your recipe in Status Kitchen
2. Enable "Add Cookbook Metadata" and fill in required fields
3. Export your recipe using "Export for Cookbook"
4. Fork this repository
5. Add your recipe folder to `recipes/`
6. Submit a pull request

## Repository Structure

```
statuskitchen-recipes/
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── recipes.json                    # Auto-generated index
├── .github/
│   └── workflows/
│       ├── validate-pr.yml         # PR validation
│       └── update-index.yml        # Auto-update index
├── scripts/
│   ├── check_uuid_uniqueness.py
│   └── generate_index.py
└── recipes/
    └── {app}-{username}-statuskitchen-app/
        ├── recipe.toml
        ├── assets/
        │   ├── {uuid}-icon.svg
        │   └── {uuid}-screenshot.png
        └── dist/
            └── {uuid}.skr
```

## Recipe Index

The `recipes.json` file is automatically generated and updated when PRs are merged. It contains metadata for all available recipes, used by the Status Kitchen app and web UI for browsing.

## License

Recipes in this repository are licensed under their individual licenses as specified in each recipe's metadata. The repository infrastructure (scripts, workflows) is licensed under the MIT License.

## Links

- [Status Kitchen](https://github.com/keithvassallomt/statuskitchen) - Main application
- [Status Kitchen Extension](https://extensions.gnome.org/extension/...) - GNOME Shell extension (coming soon)
- [Web UI](https://statuskitchen.app) - Browse recipes online (coming soon)
