from ._lupo import actions as _actions

globals().update(_actions.__dict__)

__all__ = _actions.__all__
