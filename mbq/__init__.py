# https://packaging.python.org/namespace_packages/#pkgutil-style-namespace-packages
import typing


__path__: typing.Iterable[str]  # https://docs.python.org/3/reference/import.html#__path__
__path__ = __import__('pkgutil').extend_path(__path__, __name__)
