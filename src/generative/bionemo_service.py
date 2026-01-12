class BioNeMoService:
    def fetch_esmfold_structure(self, sequence: str):
        # En la realidad, aquí haríamos un POST a la API de NVIDIA
        # Por ahora, devolvemos un PDB genérico de prueba y un score
        mock_pdb = "HEADER    PROTEIN DATA BANK..." # Contenido PDB real iría aquí
        return HormokineStructure(
            pdb_content=mock_pdb,
            plddt_score=88.5,
            molecular_weight=24.5,
            is_folded=True
        )
