#!/bin/bash

# Define the .gitattributes file path
GITATTRIBUTES_FILE=".gitattributes"

# Check if .gitattributes exists, if not, create it
if [ ! -f "$GITATTRIBUTES_FILE" ]; then
    echo "# Creating .gitattributes file"
    touch "$GITATTRIBUTES_FILE"
fi

# Add Git LFS tracking for large files
echo "# Adding Git LFS rules..."
echo "*.pkl filter=lfs diff=lfs merge=lfs" >> "$GITATTRIBUTES_FILE"
echo "*.csv filter=lfs diff=lfs merge=lfs" >> "$GITATTRIBUTES_FILE"

# Ensure consistent line endings for cross-OS development
echo "# Enforcing consistent line endings..."
echo "* text=auto" >> "$GITATTRIBUTES_FILE"

# Prevent unwanted merge conflicts on binary files
echo "# Marking binary files..."
echo "*.pkl binary" >> "$GITATTRIBUTES_FILE"
echo "*.jpg binary" >> "$GITATTRIBUTES_FILE"
echo "*.png binary" >> "$GITATTRIBUTES_FILE"

# Lock important config files to prevent multiple edits
echo "# Locking critical files..."
echo "config.json lockable" >> "$GITATTRIBUTES_FILE"

# Display the final .gitattributes file content
echo "Updated .gitattributes:"
cat "$GITATTRIBUTES_FILE"

# Add changes to Git, commit, and push
echo "# Staging, committing, and pushing to Git..."
git add "$GITATTRIBUTES_FILE"
git commit -m "Updated .gitattributes with Git LFS rules, line endings, and binary settings"
git push origin main

echo "Update completed successfully!"
