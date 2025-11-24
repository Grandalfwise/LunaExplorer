import os
import importlib

# Get directory of this file
package_dir = os.path.dirname(__file__)

print("[HANDLERS] Autoload start")

for filename in os.listdir(package_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = f"{__name__}.{filename[:-3]}"
        print(f"[HANDLERS] Importing {module_name}")
        importlib.import_module(module_name)

print("[HANDLERS] Autoload complete")