"""Week 0: check that the Python environment is ready.

Run:
    python src/check_env.py
"""

import importlib
import sys

REQUIRED = [
    ("numpy", "numpy"),
    ("pandas", "pandas"),
    ("sklearn", "scikit-learn"),
    ("matplotlib", "matplotlib"),
    ("seaborn", "seaborn"),
    ("datasets", "datasets"),
    ("lifelines", "lifelines"),
    ("xgboost", "xgboost"),
]

OPTIONAL = [
    ("torch", "pytorch (install in week 4)"),
]


def main() -> None:
    print("Python:", sys.version)
    print("-" * 60)

    missing = []
    for module_name, package_name in REQUIRED:
        try:
            module = importlib.import_module(module_name)
            version = getattr(module, "__version__", "unknown")
            print(f"[OK]      {package_name:<20} {version}")
        except Exception as exc:  # noqa: BLE001
            missing.append(package_name)
            print(f"[MISSING] {package_name:<20} {exc}")

    for module_name, package_name in OPTIONAL:
        try:
            module = importlib.import_module(module_name)
            version = getattr(module, "__version__", "unknown")
            print(f"[OK-OPT]  {package_name:<20} {version}")
        except Exception:
            print(f"[OPT]     {package_name:<20} not installed (fine for week 0)")

    print("-" * 60)

    try:
        import torch

        print("CUDA available:", torch.cuda.is_available())
        if torch.cuda.is_available():
            print("GPU:", torch.cuda.get_device_name(0))
    except Exception:
        pass

    if missing:
        print("\nMissing required packages:", ", ".join(missing))
        print("Try: conda env update -f environment.yml --prune")
    else:
        print("\nAll required packages are installed.")
        print("PyTorch is optional until week 4.")


if __name__ == "__main__":
    main()
