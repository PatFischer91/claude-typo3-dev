#!/usr/bin/env bash
# Load TYPO3 Development Standards for SessionStart hook
# This script reads the external development_standards.md file

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STANDARDS_FILE="$SCRIPT_DIR/development_standards.md"

# Check if file exists
if [ ! -f "$STANDARDS_FILE" ]; then
  echo "ERROR: Development standards file not found at $STANDARDS_FILE" >&2
  exit 1
fi

# Output the complete prompt
cat << 'HEADER'
Apply the following TYPO3 Coding Guidelines throughout this session:

HEADER

cat "$STANDARDS_FILE"

cat << 'FOOTER'


These guidelines are based on TYPO3 CGL and PSR-12. Apply them automatically when writing or reviewing code.
FOOTER

exit 0
