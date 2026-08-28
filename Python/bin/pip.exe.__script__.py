import sys

# Avoid letting __main__.__file__ lead back to this script
try:
    __file__ = None
except Exception:
    pass

# Also clear __spec__.origin when it exists
try:
    __spec__.origin = None
except Exception:
    pass

# Replace argv[0] with our executable instead of the script name.
try:
    if sys.argv[0][-14:].upper() == ".__SCRIPT__.PY":
        sys.argv[0] = sys.argv[0][:-14]
except AttributeError:
    pass
except IndexError:
    pass

if __name__ == "__main__":
    try:
        if not sys.path[0]:
            del sys.path[0]
    except AttributeError:
        pass
    except IndexError:
        pass

    from pip._internal.cli.main import main
    sys.exit(main())
