from functools import cache
from kadishutu.tools.eprint import eprintf
import re
import semver
import sys
from typing import Any, Dict

from .generic_early import CommandInstallHandler


class PipxInstallHandler(CommandInstallHandler):
    IDENT = "pipx"

    @classmethod
    def likelyness(cls) -> float:
        if cls.IDENT in __file__:
            return 80.0
        else:
            return 0.0

    @property
    @cache
    def install_venv(self) -> str:
        m = re.match(r'^.+\/venvs\/([^\/]+)\/.*$', sys.orig_argv[0])
        assert m, "Pipx virtual environment regex match failed"
        return m.group(1)

    def constraint_conv(self, k: str, v: Any) -> str:
        if v is None:
            return k
        constraint = ""
        if isinstance(v, str) and v.startswith("^"):
            semv = v[1:]
            semvv = semver.Version.parse(semv)
            constraint = f">={semv},<{semvv.major + 1}.0.0"
        else:
            eprintf(
                "WARNING: Skipping constraint {} for dependency {}",
                v, k,
            )
        # TODO: Properly handle constraints
        return k + constraint

    def install(self, deps: Dict[str, Any]):
        self.run([
            "inject", self.install_venv,
            *self.into_constrained(deps),
        ])
