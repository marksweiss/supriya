import collections
from supriya import utils
from supriya.patterns.EventPattern import EventPattern


class Pbindf(EventPattern):
    """
    Overwrites keys in an event pattern.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_event_pattern',
        '_patterns',
        )

    ### INITIALIZER ###

    def __init__(self, event_pattern=None, **patterns):
        import supriya.patterns
        assert isinstance(event_pattern, supriya.patterns.Pattern)
        self._event_pattern = event_pattern
        self._patterns = tuple(sorted(patterns.items()))

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self.patterns[item]

    ### PRIVATE METHODS ###

    def _coerce_pattern_pairs(self, patterns):
        import supriya.patterns
        patterns = dict(patterns)
        for name, pattern in sorted(patterns.items()):
            if not isinstance(pattern, supriya.patterns.Pattern):
                pattern = supriya.patterns.Pseq([pattern], None)
            patterns[name] = iter(pattern)
        return patterns

    def _iterate(self, state=None):
        should_stop = self.PatternState.CONTINUE
        event_iterator = iter(self._event_pattern)
        key_iterators = self._coerce_pattern_pairs(self._patterns)
        template_dict = {}
        while True:
            try:
                if not should_stop:
                    expr = next(event_iterator)
                else:
                    expr = event_iterator.send(True)
            except StopIteration:
                return
            expr = self._coerce_iterator_output(expr)
            for name, key_iterator in sorted(key_iterators.items()):
                try:
                    template_dict[name] = next(key_iterator)
                except StopIteration:
                    continue
            expr = utils.new(expr, **template_dict)
            should_stop = yield expr

    ### PUBLIC PROPERTIES ###

    @property
    def arity(self):
        arity = max(self._get_arity(v) for _, v in self._patterns)
        return max([self._get_arity(self._event_pattern), arity])

    @property
    def event_pattern(self):
        return self._event_pattern

    @property
    def is_infinite(self):
        import supriya.patterns
        if not self._event_pattern.is_infinite:
            return False
        for _, value in self._patterns:
            if (
                isinstance(value, supriya.patterns.Pattern) and
                not value.is_infinite
                ):
                return False
            elif isinstance(value, collections.Sequence):
                return False
        return True

    @property
    def patterns(self):
        return dict(self._patterns)
