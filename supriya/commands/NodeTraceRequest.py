from supriya.commands.Request import Request
from supriya.commands.RequestId import RequestId


class NodeTraceRequest(Request):

    ### CLASS VARIABLES ###

    __slots__ = ()

    request_id = RequestId.NODE_TRACE

    ### INITIALIZER ###

    def __init__(self):
        Request.__init__(self)
        raise NotImplementedError

    ### PUBLIC METHODS ###

    def to_osc(self, with_request_name=False):
        raise NotImplementedError
