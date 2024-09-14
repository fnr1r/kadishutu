from ..shared.editors import AbsoulteDispatcher, U8Editor
from .affinities import AffinityManager
from .potentials import PotentialEditor
from .skills import SkillEditor, SkillManager
from .stats import HealableEditor, StatBlockEditor


class DemonLikeEditor:
    stats: AbsoulteDispatcher[StatBlockEditor]
    healable: AbsoulteDispatcher[HealableEditor]
    level: U8Editor
    skills: AbsoulteDispatcher[SkillManager]
    affinities: AbsoulteDispatcher[AffinityManager]
    potentials: AbsoulteDispatcher[PotentialEditor]
    innate_skill: AbsoulteDispatcher[SkillEditor]