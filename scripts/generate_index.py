#!/usr/bin/env python3
"""
Generate recipes.json index from all recipes in the recipes/ directory.
Used by the update-index.yml workflow.
"""

import json
import os
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path

GITHUB_RAW_BASE = "https://raw.githubusercontent.com/keithvassallomt/statuskitchen-recipes/main"


def get_uuid_from_recipe(recipe: dict, folder_name: str) -> str:
    """Extract or generate UUID from recipe data."""
    # Try to get UUID from metadata section
    if "metadata" in recipe and "uuid" in recipe["metadata"]:
        return recipe["metadata"]["uuid"]

    # Generate from app name and sk_metadata
    app_name = recipe.get("app", {}).get("name", "")
    if not app_name:
        # Fall back to folder name
        return folder_name.replace("-", "@", 1).replace("-", ".")

    safe_id = "".join(c for c in app_name.lower() if c.isalnum() or c == "-")

    github_username = recipe.get("sk_metadata", {}).get("github_username")
    if github_username:
        return f"{safe_id}@{github_username}.statuskitchen.app"

    return f"{safe_id}@statuskitchen.app"


def simplified_uuid(uuid: str) -> str:
    """Convert UUID to filesystem-friendly format."""
    return uuid.replace("@", "-").replace(".", "-")


def find_asset(assets_dir: Path, uuid: str, extension: str) -> str | None:
    """Find an asset file with the given extension."""
    simplified = simplified_uuid(uuid)

    # Try exact match first
    exact_match = assets_dir / f"{simplified}-{extension.lstrip('.')}"
    if exact_match.exists():
        return exact_match.name

    # Try with icon/screenshot suffix
    for suffix in ["icon", "screenshot"]:
        pattern_file = assets_dir / f"{simplified}-{suffix}.{extension.lstrip('.')}"
        if pattern_file.exists():
            return pattern_file.name

    # Fall back to any file with that extension
    for f in assets_dir.glob(f"*.{extension.lstrip('.')}"):
        return f.name

    return None


def process_recipe(recipe_folder: Path) -> dict | None:
    """Process a single recipe folder and return index entry."""
    recipe_toml = recipe_folder / "recipe.toml"
    if not recipe_toml.exists():
        print(f"Skipping {recipe_folder.name}: no recipe.toml", file=sys.stderr)
        return None

    try:
        with open(recipe_toml, "rb") as f:
            recipe = tomllib.load(f)
    except Exception as e:
        print(f"Error parsing {recipe_toml}: {e}", file=sys.stderr)
        return None

    folder_name = recipe_folder.name
    uuid = get_uuid_from_recipe(recipe, folder_name)
    simplified = simplified_uuid(uuid)

    # Get metadata
    app = recipe.get("app", {})
    metadata = recipe.get("metadata", {})
    sk_metadata = recipe.get("sk_metadata", {})

    # Find .skr file
    dist_dir = recipe_folder / "dist"
    skr_file = None
    if dist_dir.exists():
        skr_files = list(dist_dir.glob("*.skr"))
        if skr_files:
            skr_file = skr_files[0].name

    if not skr_file:
        print(f"Skipping {folder_name}: no .skr file", file=sys.stderr)
        return None

    # Find assets
    assets_dir = recipe_folder / "assets"
    icon_file = None
    screenshot_file = None
    if assets_dir.exists():
        icon_file = find_asset(assets_dir, uuid, "svg")
        screenshot_file = find_asset(assets_dir, uuid, "png")

    # Build entry
    entry = {
        "uuid": uuid,
        "name": metadata.get("name") or app.get("name", folder_name),
        "description": metadata.get("description", ""),
        "version": metadata.get("version", 1),
        "author": sk_metadata.get("author", ""),
        "author_url": sk_metadata.get("author_url", ""),
        "license": sk_metadata.get("license", "MIT"),
        "download_url": f"{GITHUB_RAW_BASE}/recipes/{folder_name}/dist/{skr_file}",
        "gnome_shell_versions": [
            str(v) for v in metadata.get("shell_versions", [])
        ],
    }

    # Add optional URLs
    if icon_file:
        entry["icon_url"] = f"{GITHUB_RAW_BASE}/recipes/{folder_name}/assets/{icon_file}"

    if screenshot_file:
        entry["screenshot_url"] = f"{GITHUB_RAW_BASE}/recipes/{folder_name}/assets/{screenshot_file}"

    # Extract tags from description or add empty list
    entry["tags"] = []

    return entry


def main():
    recipes_dir = Path("recipes")
    if not recipes_dir.exists():
        print("No recipes directory found, creating empty index")
        recipes_dir.mkdir(exist_ok=True)

    # Process all recipes
    entries = []
    for recipe_folder in sorted(recipes_dir.iterdir()):
        if not recipe_folder.is_dir():
            continue
        if recipe_folder.name.startswith("."):
            continue

        entry = process_recipe(recipe_folder)
        if entry:
            entries.append(entry)

    # Generate index
    index = {
        "version": 1,
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "recipes": entries,
    }

    # Write index
    with open("recipes.json", "w") as f:
        json.dump(index, f, indent=2)

    print(f"Generated recipes.json with {len(entries)} recipes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
