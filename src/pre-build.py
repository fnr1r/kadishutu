from os import link
from pathlib import Path
from shutil import copy2
import toml


PYPROJ = "pyproject.toml"


def main():
    # We need access to opt-depends when running the app.
    # Nuclear solution: copy pyproject.toml
    # The downside of using a build script is that wheels now have an assigned
    # platform despite being literally the f**king same
    # There should be an option NOT to do this
    print(f"Copying {PYPROJ} to depinstall tool")
    here = Path.cwd()
    proj = here / PYPROJ
    with proj.open("r", encoding="UTF-8") as file:
        data = toml.load(file)
    target = here / "src/{}/tools/depinstall/{}".format(
        data["tool"]["poetry"]["name"], PYPROJ,
    )
    if target.exists():
        if proj.stat().st_ino == target.stat().st_ino:
            print(f"{PYPROJ} is hard-linked. Skipping")
            return
        copy2(proj, target)
    else:
        try:
            link(proj, target)
        except OSError as e:
            print("Trying to hard-link failed:", repr(e))
            copy2(proj, target)


if __name__ == "__main__":
    main()
