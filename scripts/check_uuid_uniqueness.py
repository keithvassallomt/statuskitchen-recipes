#!/usr/bin/env python3
"""
Check that all recipe UUIDs are unique.
Used by the validate-pr.yml workflow.
"""

import json
import os
import sys
import tomllib
from pathlib import Path


def get_uuid_from_recipe(recipe_path: Path) -> str | None:
    """Extract UUID from a recipe.toml file."""
    try:
        with open(recipe_path, "rb") as f:
            recipe = tomllib.load(f)

        # Try to get UUID from metadata section
        if "metadata" in recipe and "uuid" in recipe["metadata"]:
            return recipe["metadata"]["uuid"]

        # Fall back to generating from app name and sk_metadata
        app_name = recipe.get("app", {}).get("name", "")
        if not app_name:
            return None

        # Generate safe ID from app name
        safe_id = "".join(
            c for c in app_name.lower() if c.isalnum() or c == "-"
        )

        # Check for github_username in sk_metadata
        github_username = recipe.get("sk_metadata", {}).get("github_username")
        if github_username:
            return f"{safe_id}@{github_username}.statuskitchen.app"

        return f"{safe_id}@statuskitchen.app"

    except Exception as e:
        print(f"Error reading {recipe_path}: {e}", file=sys.stderr)
        return None


def main():
    recipes_dir = Path("recipes")
    if not recipes_dir.exists():
        print("No recipes directory found")
        return 0

    # Collect all UUIDs
    uuid_to_folder: dict[str, list[str]] = {}

    for recipe_folder in recipes_dir.iterdir():
        if not recipe_folder.is_dir():
            continue

        recipe_toml = recipe_folder / "recipe.toml"
        if not recipe_toml.exists():
            continue

        uuid = get_uuid_from_recipe(recipe_toml)
        if uuid:
            if uuid not in uuid_to_folder:
                uuid_to_folder[uuid] = []
            uuid_to_folder[uuid].append(recipe_folder.name)

    # Check for duplicates
    duplicates = {
        uuid: folders
        for uuid, folders in uuid_to_folder.items()
        if len(folders) > 1
    }

    if duplicates:
        print("::error::Duplicate UUIDs found!")
        for uuid, folders in duplicates.items():
            print(f"  UUID '{uuid}' appears in: {', '.join(folders)}")
        return 1

    print(f"UUID uniqueness check passed: {len(uuid_to_folder)} unique recipes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
