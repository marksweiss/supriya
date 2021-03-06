import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class OffsetOut(UGen):
    """
    A bus output unit generator with sample-accurate timing.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> supriya.ugens.OffsetOut.ar(
        ...     bus=0,
        ...     source=source,
        ...     )
        OffsetOut.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Input/Output UGens'

    _default_channel_count = 0

    _is_output = True

    _ordered_input_names = collections.OrderedDict([
        ('bus', 0),
        ('source', None),
    ])

    _unexpanded_input_names = (
        'source',
    )

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
    )
