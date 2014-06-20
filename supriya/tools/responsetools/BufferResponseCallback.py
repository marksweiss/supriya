# -*- encoding: utf-8 -*-
from supriya.tools.osctools.OscCallback import OscCallback


class BufferResponseCallback(OscCallback):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_server',
        '_response_manager',
        )

    ### INITIALIZER ###

    def __init__(self, server):
        from supriya.tools import servertools
        OscCallback.__init__(
            self,
            address_pattern='/b_(info|set|setn)',
            procedure=self.__call__,
            )
        assert isinstance(server, servertools.Server)
        self._server = server
        self._response_manager = server._response_manager

    ### SPECIAL METHODS ###

    def __call__(self, message):
        from supriya.tools import servertools
        #print(message)
        response = self._response_manager(message)
        if not isinstance(response, tuple):
            response = (response,)
        for x in response:
            #print(x)
            buffer_id = x.buffer_id
            buffer_proxy = self._server._buffer_proxies.get(buffer_id)
            if not buffer_proxy:
                buffer_proxy = servertools.BufferProxy(
                    buffer_id=buffer_id,
                    server=self._server,
                    )
                self._server._buffer_proxies[buffer_id] = buffer_proxy
            buffer_proxy.handle_response(x)
