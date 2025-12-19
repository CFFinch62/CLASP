try:
    from clasp.pylogo.interpreter import Logo
    print("PyLogo imported successfully from vendored package.")
except ImportError as e:
    print(f"Failed to import PyLogo: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
