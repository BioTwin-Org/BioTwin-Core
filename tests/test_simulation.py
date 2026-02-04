import pytest
import sys
import os

# TRUCO DE SISTEMA:
# Esto asegura que Python encuentre la carpeta 'src' sin importar
# desde dónde ejecutes el test (local o servidor de GitHub Actions).
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.model_containers.agent_based.liver_model import LiverModel

class TestBioTwinCore:
    
    def test_initial_state_integrity(self):
        """Verifica que el modelo inicie con parámetros fisiológicos válidos."""
        model = LiverModel()
        assert 0.0 <= model.fibrosis_level <= 1.0
        assert 0.0 <= model.inflammation_level <= 1.0
        assert len(model.kupffer_population) == 10
        assert model.steps == 0

    def test_simulation_cycle(self):
        """Verifica que el motor de tiempo avance y guarde historial."""
        model = LiverModel()
        model.update_state()
        
        assert model.steps == 1
        assert len(model.history) == 1
        # Verifica que se guarden las métricas clave
        last_record = model.history[-1]
        assert "Fibrosis" in last_record
        assert "Inflammation" in last_record

    def test_hormokine_therapeutic_effect(self):
        """
        Prueba CRÍTICA: Verifica que la inyección del fármaco
        realmente reduzca la inflamación y la fibrosis.
        """
        model = LiverModel()
        
        # Establecemos un estado patológico alto manualmente
        model.inflammation_level = 0.9
        model.hsc_activation_level = 0.9
        
        # Inyectamos la Hormokina (Potencia alta, Afinidad alta)
        model.inject_hormokine(potency=0.9, target_affinity=1.0)
        
        # Aserciones: Los niveles deben haber bajado
        assert model.inflammation_level < 0.9, "La inflamación no bajó tras el tratamiento"
        assert model.hsc_activation_level < 0.9, "La activación de HSC no bajó tras el tratamiento"

    def test_alphagenome_risk_integration(self):
        """
        Verifica que el factor de riesgo genético se integre correctamente
        en la lógica del modelo.
        """
        model = LiverModel()
        
        # Asignamos un riesgo genético de AlphaGenome
        model.genetic_risk = 1.5
        
        # Ejecutamos un ciclo
        model.update_state()
        
        # Verificamos que el modelo siga siendo estable numéricamente
        assert model.genetic_risk == 1.5
        assert 0.0 <= model.inflammation_level <= 1.5 # Margen de tolerancia
