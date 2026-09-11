# Project-specific configuration for the generic poetry Makefile.
# This is the only file that changes per project — the Makefile itself
# is synced from skel/pylib and must not be edited.

# Source code path(s) for style linters (isort, black, flake8,
# pycodestyle, pylint). A directory (mypackage/), several paths
# (mypackage tests) or a single file (mymodule.py).
CODE = pytaboola

# Path(s) for type checking with mypy. Defaults to CODE if unset.
# TYPE_CODE = pytaboola

# Test command. Defaults to `poetry run pytest` if unset.
# TEST_CMD = poetry run pytest tests/

# Linter flags — these relax rules but never skip a linter.
PYCODESTYLE_IGNORE = E126,E127,E128,W503
PYLINT_DISABLE     = I0011,R0901,R0902,R0801,C0111,C0103,C0411,C0415,R0903,R0913,R0914,R0915,R1710,W0613,W0703

# Git tag prefix for `make release`: set to `v` for vX.Y.Z tags,
# leave empty for plain X.Y.Z tags.
TAG_PREFIX =

# Publish target — a Poetry repository name, configured once on the
# machine that publishes, with `poetry config repositories.<name>
# <url>`. The URL is deliberately not written down here: this repo
# is public.
# Leave empty ONLY for packages meant to be public on pypi.org.
PUBLISH_REPOSITORY =
