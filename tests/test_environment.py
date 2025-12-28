# tests/test_environment.py

def test_python_environment():
    """Verifica que el entorno de ejecución básico está activo."""
    assert True

def test_biotwin_imports():
    """
    Prueba que los módulos core son detectables.
    A medida que agregues código a /src, este test crecerá.
    """
    try:
        # Esto es solo un marcador de posición para futuros módulos
        import sys
        assert "sys" in sys.modules
    except ImportError:
        assert False
