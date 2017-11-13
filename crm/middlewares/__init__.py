"""
Import and expose all modules in this package.
Now any added module/command will be exposed automatically
"""

import pkgutil
import inspect
import os

__all__ = []

for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    excluded_middlewares = [md.strip() for md in os.getenv('EXCLUDED_MIDDLEWARES', '').split(',')]
    if name in excluded_middlewares:
        continue

    module = loader.find_module(name).load_module(name)

    for name, value in inspect.getmembers(module):
        if name.startswith('__'):
            continue

        globals()[name] = value
        __all__.append(name)
