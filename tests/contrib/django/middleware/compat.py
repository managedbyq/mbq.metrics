import sys


IS_PYTHON3 = sys.version_info[0] >= 3

try:
    from unittest import mock
except ImportError:
    import mock  # noqa


def mock_open_patch(file_contents):
    patch_target = 'builtins.open' if IS_PYTHON3 else '__builtin__.open'
    return mock.patch(patch_target, mock.mock_open(read_data=file_contents))
