class MixinContextDecorator(object):
    def __init__(self, val=None):
        self.__val = val

    def __call__(self, obj, extra=''):
        if type(obj) == type:
            # handle class decoration
            class NewClass(obj):
                def __getattribute__(self_internal, item):
                    original = super(obj, self_internal).__getattribute__(item)

                    if not callable(original) or (item.startswith('__') and item.endswith('__')):
                        return original

                    return self(original, obj.__name__)

            return NewClass

        context_manager = self.__class__(obj.func_name + extra) if self.__val is None else self
        def wrapper(*args, **kwargs):
            with context_manager:
                return obj(*args, **kwargs)
        return wrapper

    def __enter__(self):
        print 'enter %s' % self.__val

    def __exit__(self, exc_type, exc_val, exc_tb):
        print 'exit %s' % self.__val

    def __getattribute__(self, item):
        original = super(MixinContextDecorator, self).__getattribute__(item)

        if not callable(original) or (item.startswith('__') and item.endswith('__')):
            return original

        def wrapper(*args, **kwargs):
            with self.__class__(item):
                return original(*args, **kwargs)

        return wrapper
