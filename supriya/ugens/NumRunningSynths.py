import collections
from supriya import CalculationRate
from supriya.ugens.InfoUGenBase import InfoUGenBase


class NumRunningSynths(InfoUGenBase):
    """
    A number of running synths info unit generator.

    ::

        >>> supriya.ugens.NumRunningSynths.ir()
        NumRunningSynths.ir()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Info UGens'

    _ordered_input_names = collections.OrderedDict()

    _valid_calculation_rates = (
        CalculationRate.CONTROL,
        CalculationRate.SCALAR,
    )
