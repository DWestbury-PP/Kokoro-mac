#!/bin/bash
# Add speak alias to shell profile

KOKORO_PATH="/Users/dwestbury/Documents/Source Code/Kokoro-Mac"
SHELL_RC="$HOME/.zshrc"

# Create the alias
ALIAS_LINE="alias speak='\"$KOKORO_PATH/.venv/bin/speak\"'"

# Check if alias already exists
if grep -q "alias speak=" "$SHELL_RC" 2>/dev/null; then
    echo "⚠️  'speak' alias already exists in $SHELL_RC"
    echo "Please remove the existing alias first, then run this script again."
    exit 1
fi

# Add the alias
echo "" >> "$SHELL_RC"
echo "# Kokoro speak command" >> "$SHELL_RC"
echo "$ALIAS_LINE" >> "$SHELL_RC"

echo "✅ Added 'speak' alias to $SHELL_RC"
echo "Restart your terminal or run: source $SHELL_RC"
echo ""
echo "Test it with:"
echo "  speak 'Hello from anywhere!' --voice af_heart"
