
class DemoAPI(object):

    def echo(self, something):
        return something

    def echo_args(self, *args, **kwargs):
        return args, kwargs


