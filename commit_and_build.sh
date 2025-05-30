#!/bin/bash

# Quick script to commit changes and trigger GitHub Actions build

echo "🚀 Committing changes and triggering build..."

# Add all files
git add .

# Commit with timestamp
git commit -m "Build real Windows executables - $(date)"

# Push to trigger GitHub Actions
git push

echo "✅ Pushed to GitHub!"
echo "🔄 GitHub Actions will now build REAL Windows executables"
echo "📱 Check progress at: https://github.com/[YOUR_USERNAME]/control-shift-game/actions"
echo ""
echo "Once complete, download the 'all-platforms-release' artifact"
echo "It will contain proper .exe files that work on Windows!" 