from abc import ABC, abstractmethod
from subprocess import Popen
from typing import Any, ClassVar, Dict, List

from .pyproj import get_opt_depends


class InstallHandler(ABC):
    IDENT: ClassVar[str]

    @classmethod
    @abstractmethod
    def likelyness(cls) -> float: ...
    @abstractmethod
    def install(self, deps: Dict[str, Any]): ...

    def install_group(self, group: str):
        self.install(get_opt_depends(group))

    def install_groups(self, *groups: str):
        for group in groups:
            self.install_group(group)


class CommandInstallHandler(InstallHandler, ABC):
    @classmethod
    def command_exists(cls) -> bool:
        try:
            Popen([cls.IDENT]).terminate()
        except FileNotFoundError:
            return False
        return True

    def constraint_conv(self, k: str, v: Any) -> str:
        return k

    def into_constrained(self, deps: Dict[str, Any]) -> List[str]:
        return [
            self.constraint_conv(k, v)
            for k, v in deps.items()
        ]

    def run(self, aargs, *args, **kwargs):
        p = Popen([self.IDENT] + aargs, *args, **kwargs)
        ret = p.wait()
        assert ret == 0, f"Exited with non-zero exit code {ret}"
