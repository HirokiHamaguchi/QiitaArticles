import shutil
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
HYPERREF_DIR = SCRIPT_DIR / "hyperref"
TEMP_DIR = SCRIPT_DIR / "temp"
OUTPUT_HYPERREF_STY = SCRIPT_DIR / "hyperref.sty"

REQUIRED_FILES = [
    HYPERREF_DIR / "hyperref.ins",
    HYPERREF_DIR / "hyperref.dtx",
    HYPERREF_DIR / "backref.dtx",
    HYPERREF_DIR / "nameref.dtx",
    HYPERREF_DIR / "hluatex.dtx",
    HYPERREF_DIR / "hyperref-linktarget.dtx",
    HYPERREF_DIR / "hyperref-patches.dtx",
    HYPERREF_DIR / "xr-hyper.dtx",
]


def run() -> None:
    missing = [str(path) for path in REQUIRED_FILES if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing required files:\n" + "\n".join(missing))

    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    hyperref_work_dir = TEMP_DIR / "hyperref"
    hyperref_work_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(HYPERREF_DIR / "hyperref.ins", hyperref_work_dir / "hyperref.ins")
    shutil.copy2(HYPERREF_DIR / "hyperref.dtx", hyperref_work_dir / "hyperref.dtx")
    shutil.copy2(HYPERREF_DIR / "backref.dtx", hyperref_work_dir / "backref.dtx")
    shutil.copy2(HYPERREF_DIR / "nameref.dtx", hyperref_work_dir / "nameref.dtx")
    shutil.copy2(HYPERREF_DIR / "hluatex.dtx", hyperref_work_dir / "hluatex.dtx")
    shutil.copy2(
        HYPERREF_DIR / "hyperref-linktarget.dtx",
        hyperref_work_dir / "hyperref-linktarget.dtx",
    )
    shutil.copy2(
        HYPERREF_DIR / "hyperref-patches.dtx",
        hyperref_work_dir / "hyperref-patches.dtx",
    )
    shutil.copy2(HYPERREF_DIR / "xr-hyper.dtx", hyperref_work_dir / "xr-hyper.dtx")

    result = subprocess.run(
        ["tex", "-interaction=nonstopmode", "hyperref.ins"],
        cwd=hyperref_work_dir,
        text=True,
        capture_output=True,
    )

    generated = hyperref_work_dir / "hyperref.sty"
    if result.returncode != 0 or not generated.exists():
        msg = "Failed to generate hyperref.sty via hyperref.ins"
        msg += "\n\n--- stdout ---\n" + result.stdout[-4000:]
        msg += "\n\n--- stderr ---\n" + result.stderr[-4000:]
        raise RuntimeError(msg)

    shutil.copy2(generated, OUTPUT_HYPERREF_STY)

    if TEMP_DIR.exists() and TEMP_DIR.is_dir():
        shutil.rmtree(TEMP_DIR)

    print(f"Generated: {OUTPUT_HYPERREF_STY}")


if __name__ == "__main__":
    run()
