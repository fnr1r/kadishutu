import os
from pathlib import Path
import platform
from subprocess import PIPE, Popen
from tarfile import TarFile, TarInfo
from typing import Any, Dict, List, Optional
from zipfile import ZIP_DEFLATED, ZipFile


TOOL_NAME = "pyinstaller-archiver"


class PyIntallerHookInterface:
    """
    Pyinstaller hook interface

    Attributes:
        _io (IO): cleo.io.io IO instance
        _venv (VirtualEnv): poetry.utils.env VirtualEnv instance
        poetry (Poetry): poetry.poetry Poetry instance
        pyproject_data (dict): pyproject.TOML contents
        platform (str): platform string
    """

    poetry: Any
    pyproject_data: Dict
    platform: str

    def run(self, command: str, *args: str) -> None:
        """Run command in virtual environment"""

    def run_pip(self, *args: str) -> None:
        """Install requirements in virtual environment"""

    def write_line(self, output: str) -> None:
        """Output message with Poetry IO"""


INTERFACE: PyIntallerHookInterface


def ifprint(
    *values: object,
    sep: Optional[str] = " ",
    interface: Optional[PyIntallerHookInterface] = None,
):
    if not interface:
        interface = INTERFACE
    if sep is None:
        sep = ""
    interface.write_line(sep.join([
        str(value)
        for value in values
    ]))


def pbuild(*args, **kwargs):
    ifprint("<b>[BUILD ]</b>", *args, **kwargs)


def pconfig(*args, **kwargs):
    ifprint("<b>[CONFIG]</b>", *args, **kwargs)


def pinfo(*args, **kwargs):
    ifprint("<b>[ INFO ]</b>", *args, **kwargs)


def exectxt(*args: str) -> str:
    ps = Popen(args, stdout=PIPE)
    assert not ps.wait()
    stdout = ps.stdout
    assert stdout
    return stdout.read().decode()[:-1]


def zip_files(source: Path, target: Path, strip_path: int = 0):
    """
    Sauce: https://gist.github.com/kgn/610907

    Well, actually no, since I'm not using zip for linux.
    """
    with ZipFile(target, "w", ZIP_DEFLATED) as ark:
        for file in source.rglob("*"):
            target_file = Path(*file.parts[strip_path:])
            ark.write(file, target_file)


def tar_anonymize(info: TarInfo) -> Optional[TarInfo]:
    info.uid = 1000
    info.uname = "build"
    info.gid = 1000
    info.gname = "build"
    return info


def xz_files(source: Path, target: Path, strip_path: int = 0):
    with TarFile.open(target, "w:xz") as ark:
        for file in source.glob("*"):
            target_file = Path(*file.parts[strip_path:])
            ark.add(file, target_file, filter=tar_anonymize)


def sevenz_files(source: Path, target: Path, strip_path: int = 0):
    # I can't get this to work.
    #INTERFACE.run_pip("install", "py7zr")
    #from py7zr import SevenZipFile
    #with SevenZipFile(target, "w") as ark:
    #    for file in source.rglob("*"):
    #        target_file = Path(*file.parts[strip_path:])
    #        ark.write(file, str(target_file))
    try:
        pinfo("Using 7z command")
        prev_path = Path(os.curdir).absolute()
        os.chdir(source)
        target = Path(os.pardir) / target.name
        if target.exists():
            target.unlink()
        ps = Popen(["7z", "u", target, "*"])
        ps.wait()
        ret = ps.returncode
        if ret != 0:
            raise RuntimeError(f"7z returned non-zero exit code {ret}")
        os.chdir(prev_path)
    except Exception as e:
        if isinstance(e, RuntimeError):
            print()
        pbuild("<fg=red>Archiving failed for 7z</fg>:", e)


def post_build(interface: PyIntallerHookInterface):
    global INTERFACE
    INTERFACE = interface
    ifprint("<b>[[ PyInstaller Archiver ]]</b>")
    config = interface.pyproject_data["tool"][TOOL_NAME]
    project_name: str = interface.pyproject_data["tool"]["poetry"]["name"]
    pconfig("Project:", project_name)
    pyinstaller_build_path = Path("dist/pyinstaller") / interface.platform
    build_path = pyinstaller_build_path / project_name
    pconfig("Build path:", build_path)
    platformstr = platform.system()
    pconfig("Platform:", platformstr, f"({interface.platform})")
    platformstr = platformstr.lower()
    short_hash = exectxt("git", "rev-parse", "--short", "HEAD")
    pconfig("Short commit hash:", short_hash)
    ark_unformatted_name = config["archive_name"]
    ark_name = ark_unformatted_name.format(
        name=project_name, platform=platformstr, commit=short_hash
    )
    formats: List[str] = config["formats"][platformstr]
    for fmt in formats:
        if fmt == "zip":
            compressor = zip_files
            extension = ".zip"
        elif fmt == "xz":
            compressor = xz_files
            extension = ".tar.xz"
        elif fmt == "7z":
            compressor = sevenz_files
            extension = ".7z"
        else:
            raise ValueError("Invalid archive format")
        ark_filename = ark_name + extension
        ark_path = pyinstaller_build_path / ark_filename
        pbuild("Building", ark_filename)
        compressor(build_path, ark_path, 4)
    pinfo("<b>Done</b>")
