from os import listdir
import os
from pathlib import Path
import platform
from subprocess import PIPE, Popen
from tarfile import TarFile, TarInfo
from typing import IO, Any, Dict, Optional
from zipfile import ZIP_DEFLATED, ZipFile

class PyInstallerPluginHook:
    _io: IO
    _venv: Any
    poetry: Any
    platform: str

    @property
    def pyproject_data(self) -> Dict: ...

    def run(self, command: str, *args: str) -> None: ...

    def run_pip(self, *args: str) -> None: ...

    def write_line(self, output: str) -> None: ...

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

def change_user(info: TarInfo) -> Optional[TarInfo]:
    info.uid = 1000
    info.uname = "build"
    info.gid = 1000
    info.gname = "build"
    return info

def xz_files(source: Path, target: Path, strip_path: int = 0):
    with TarFile.open(target, "w:xz") as ark:
        for file in source.glob("*"):
            target_file = Path(*file.parts[strip_path:])
            ark.add(file, target_file, filter=change_user)

def post_build(pyinstaller_hook: PyInstallerPluginHook):
    path = Path("dist/pyinstaller")
    path /= listdir(path)[0]
    dir_path = path / "kadishutu"
    pyinstaller_hook.write_line(f"Zipping {dir_path}")
    platformstr = platform.system()
    pyinstaller_hook.write_line("Platform: " + platformstr)
    short_hash = exectxt("git", "rev-parse", "--short", "HEAD")
    pyinstaller_hook.write_line("Commit hash: " + short_hash)
    if os.name == "nt":
        compressor = zip_files
        extension = "zip"
    else:
        compressor = xz_files
        extension = "tar.xz"
    zip_path = path / "kadishutu-{}-{}.{}".format(
        platformstr.lower(), short_hash, extension
    )
    pyinstaller_hook.write_line("Archive path: " + str(zip_path))
    compressor(dir_path, zip_path, 4)
