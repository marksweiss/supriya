from supriya.library.audiolib.UGen import UGen
from supriya.library.audiolib import ArgumentSpecification


class Line(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        ArgumentSpecification('start', 0),
        ArgumentSpecification('end', 1),
        ArgumentSpecification('dur', 1),
        ArgumentSpecification('doneAction', 0),
        )