# Contributing to Status Kitchen Recipes

Thank you for contributing to the Status Kitchen cookbook! This guide will help you submit your recipe.

## Before You Start

1. **Test your recipe thoroughly** - Make sure it works correctly with the target application
2. **Use the latest Status Kitchen** - Ensure you're using a recent version
3. **Check for duplicates** - Search existing recipes to avoid duplicating work

## Creating Your Recipe

### Step 1: Create the Recipe in Status Kitchen

1. Open Status Kitchen
2. Click "New Recipe" or edit an existing one
3. Configure your recipe:
   - **App Name**: The application name (e.g., "Nextcloud")
   - **App ID**: Unique identifier derived from the name
   - **D-Bus Pattern**: Pattern to match the application's D-Bus name (e.g., `*nextcloud*`)
   - **Icon Configuration**: Set up static/dynamic icons
   - **Menu Items**: Configure which menu items to expose

### Step 2: Add Cookbook Metadata

1. Enable the "Add Cookbook Metadata" toggle
2. Fill in all required fields:
   - **GitHub Username**: Your GitHub username (used for UUID)
   - **Extension UUID**: Auto-generated, but can be customized
   - **Author Name**: Your name or handle
   - **Author URL**: Link to your profile (auto-filled from GitHub username)
   - **License**: Choose an appropriate license
   - **Recipe Repository**: Auto-generated link to your recipe folder
   - **Extension Name**: Display name for the extension
   - **Description**: Brief description of what the recipe does
   - **Version**: Start at 1, increment for updates
   - **Shell Versions**: Check all compatible GNOME Shell versions

### Step 3: Add Assets

- **Extension Icon**: SVG icon for the extension (optional, placeholder used if not provided)
- **Screenshot**: PNG screenshot showing the indicator in action (recommended)

### Step 4: Export for Cookbook

1. Click "Export for Cookbook" in Status Kitchen
2. This creates a folder with the correct structure:
   ```
   {app}-{username}-statuskitchen-app/
   ├── recipe.toml
   ├── assets/
   │   ├── {uuid}-icon.svg
   │   └── {uuid}-screenshot.png
   └── dist/
       └── {uuid}.skr
   ```

## Submitting Your Recipe

### Step 1: Fork the Repository

1. Fork [keithvassallomt/statuskitchen-recipes](https://github.com/keithvassallomt/statuskitchen-recipes)
2. Clone your fork locally

### Step 2: Add Your Recipe

1. Copy your exported recipe folder to the `recipes/` directory
2. Verify the folder structure matches the expected format

### Step 3: Verify Your Submission

Run these checks locally:

```bash
# Check TOML is valid
python3 -c "import tomllib; tomllib.load(open('recipes/YOUR_FOLDER/recipe.toml', 'rb'))"

# Check .skr is valid ZIP
unzip -t recipes/YOUR_FOLDER/dist/*.skr

# Check required files exist
ls recipes/YOUR_FOLDER/recipe.toml
ls recipes/YOUR_FOLDER/assets/
ls recipes/YOUR_FOLDER/dist/*.skr
```

### Step 4: Submit a Pull Request

1. Commit your changes with a descriptive message
2. Push to your fork
3. Create a pull request against the `main` branch
4. Fill in the PR template

## Pull Request Requirements

Your PR will be automatically validated. It must pass these checks:

1. **Structure Validation**
   - `recipe.toml` exists and parses correctly
   - `assets/` directory exists
   - `dist/*.skr` file exists and is a valid ZIP archive

2. **UUID Uniqueness**
   - Your recipe's UUID must not conflict with existing recipes
   - UUID format: `{app}@{github_username}.statuskitchen.app`

3. **Folder Naming**
   - Folder name must match simplified UUID: `{app}-{username}-statuskitchen-app`

## Recipe Guidelines

### Do

- Target one specific application per recipe
- Use descriptive names and descriptions
- Include a screenshot showing the indicator working
- Test on multiple GNOME Shell versions if possible
- Keep menu items relevant and useful

### Don't

- Submit recipes for applications that don't use tray icons
- Include sensitive information in recipes
- Submit duplicate recipes for the same application
- Use offensive or inappropriate names/descriptions

## Updating Your Recipe

To update an existing recipe:

1. Increment the version number in Status Kitchen
2. Export the updated recipe
3. Replace the files in your fork
4. Submit a new PR with the changes

The version number must be higher than the current published version.

## License

By submitting a recipe, you agree that:

1. Your recipe will be published under the license you specify
2. The recipe metadata will be included in the public recipes.json index
3. Others may install and use your recipe via Status Kitchen

## Getting Help

- **Issues**: [Status Kitchen Issues](https://github.com/keithvassallomt/statuskitchen/issues)
- **Discussions**: [Status Kitchen Discussions](https://github.com/keithvassallomt/statuskitchen/discussions)

## Code of Conduct

Please be respectful and constructive in all interactions. We want this to be a welcoming community for everyone.
