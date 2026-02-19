#!/bin/sh
ollama serve &  # Start Ollama in the background
sleep 2         # Wait for it to initialize
ollama pull deepseek-r1  # Pull Deepseek R1 model
tail -f /dev/null  # Keep the container running
