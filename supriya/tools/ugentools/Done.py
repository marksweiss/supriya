# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Done(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_argument_names = (
        'source',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        source=None,
        ):
        assert isinstance(source, UGen)
        assert source.has_done_action
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        source=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen