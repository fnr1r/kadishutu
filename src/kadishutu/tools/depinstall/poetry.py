from kadishutu.tools.eprint import eprintf
import os
from typing import Any, Dict

from .generic_early import CommandInstallHandler
from .pyproj import get_groups


class PoetryInstallHandler(CommandInstallHandler):
    IDENT = "poetry"
    GROUP_NAME = "self-managed"

    @classmethod
    def likelyness(cls) -> float:
        if "VIRTUAL_ENV" in os.environ:
            return 90.0
        else:
            return 0.0

    def constraint_conv(self, k: str, v: Any) -> str:
        if v is None:
            return k
        constraint = ""
        if isinstance(v, str):
            constraint = "@" + v
        else:
            eprintf(
                "WARNING: Skipping constraint {} for dependency {}",
                v, k,
            )
        # TODO: Properly handle constraints
        return k + constraint

    def install(self, deps: Dict[str, Any]):
        self.run([
            "add", "--lock", "--no-interaction",
            "--group", self.GROUP_NAME,
            *self.into_constrained(deps),
        ])

    def install_group(self, group: str):
        return self.install_groups(group)

    def install_groups(self, *groups: str):
        proj_groups = get_groups()
        cmd = ["install", "--no-interaction"]

        def gflag_add(flag: str, val: bool):
            grps = [
                i
                for i in proj_groups
                if (i in groups) == val
            ]
            if not grps:
                return
            cmd.extend([flag, ",".join(grps)])

        gflag_add("--without", False)
        gflag_add("--with", True)
        self.run(cmd)
