#!/bin/bash
# Install script to make 'speak' command available system-wide

KOKORO_PATH="/Users/dwestbury/Documents/Source Code/Kokoro-Mac"
WRAPPER_SCRIPT="/usr/local/bin/speak"

# Create the wrapper script
sudo tee "$WRAPPER_SCRIPT" > /dev/null << 'EOF'
#!/bin/bash
# Global wrapper for Kokoro speak command
KOKORO_PATH="/Users/dwestbury/Documents/Source Code/Kokoro-Mac"
exec "$KOKORO_PATH/.venv/bin/speak" "$@"
EOF

# Make it executable
sudo chmod +x "$WRAPPER_SCRIPT"

echo "✅ Global 'speak' command installed to $WRAPPER_SCRIPT"
echo "You can now use 'speak' from anywhere in your terminal!"
echo ""
echo "Test it with:"
echo "  speak 'Hello from anywhere!' --voice af_heart"
