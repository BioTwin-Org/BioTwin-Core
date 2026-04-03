# tests/test_simulation.py
import pytest
from src.model_containers.agent_based.liver_model import LiverModel

def test_initial_state():
    """Verifica que el modelo inicie con los valores patológicos correctos"""
    model = LiverModel()
    assert model.fibrosis_level == 0.85
    assert model.inflammation_level == 0.80
    assert len(model.kupffer_cells) == 5

def test_model_update_cycle():
    """Verifica que un paso de simulación actualice el historial y los estados"""
    model = LiverModel()
    model.update_state()
    assert model.steps == 1
    assert len(model.history) == 1
    # Verificamos que los valores se mantengan en el rango [0, 1]
    assert 0 <= model.fibrosis_level <= 1

def test_hormokine_impact():
    """Verifica que la inyección de Hormokina reduzca la inflamación"""
    model = LiverModel()
    initial_inf = model.inflammation_level
    
    # Simulamos inyección con potencia alta
    model.inject_hormokine(potency=0.9)
    
    assert model.inflammation_level < initial_inf
    assert model.hsc_activation_level < 0.90

def test_kupffer_polarization():
    """Verifica que las células de Kupffer cambien de estado según la salud"""
    model = LiverModel()
    # Forzamos un estado saludable
    model.hepatocyte_viability = 0.9
    model.hsc_activation_level = 0.1
    
    # Ejecutamos ciclo para que las Kupffer 'censar' el nuevo estado
    model.update_state()
    
    # El promedio de inflamación debería empezar a bajar hacia M2
    assert model.inflammation_level < 0.80
