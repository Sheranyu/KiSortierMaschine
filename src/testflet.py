import micropip

async def install_opencv():
    await micropip.install("opencv-python")

# Führe die Funktion aus
await install_opencv()
