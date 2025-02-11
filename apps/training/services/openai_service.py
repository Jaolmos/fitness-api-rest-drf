import json
from typing import Dict, Any
from openai import OpenAI
from django.conf import settings
from django.core.exceptions import ValidationError


class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-3.5-turbo"
        self.temperature = 0.7

    def _create_prompt(self, experience_level: str, fitness_goal: str,
                       available_days: int, health_conditions: str = None) -> str:
        """Crea el prompt para OpenAI"""

        base_prompt = f"""Actúa como un entrenador personal profesional experto en crear planes de entrenamiento.
        
        Necesito un plan de entrenamiento con estas características:
        - Nivel de experiencia: {experience_level}
        - Objetivo: {fitness_goal}
        - Días disponibles: {available_days}
        {f'- Condiciones de salud a considerar: {health_conditions}' if health_conditions else ''}

        El plan debe seguir estas pautas:
        1. Estructura óptima según el nivel y objetivo
        2. Ejercicios específicos con series, repeticiones y descanso
        3. Progresión adecuada
        4. Consideraciones de seguridad
        
        Devuelve SOLO un JSON con esta estructura exacta:
        {
            "dias": [
                {
                "dia": "nombre del día",
                    "ejercicios": [
                        {
                    "nombre": "nombre del ejercicio",
                            "series": "número de series",
                            "repeticiones": "rango de repeticiones",
                            "descanso": "tiempo en segundos"
                        }
                    ]
                }
            ]
        }
        
        NO incluyas ningún texto adicional, SOLO el JSON."""

        return base_prompt

    def _validate_response(self, response: Dict) -> bool:
        """Valida que la respuesta tenga la estructura correcta"""
        try:
            if not isinstance(response, dict):
                return False
            if 'dias' not in response:
                return False
            if not isinstance(response['dias'], list):
                return False

            for dia in response['dias']:
                if not all(key in dia for key in ['dia', 'ejercicios']):
                    return False
                if not isinstance(dia['ejercicios'], list):
                    return False

                for ejercicio in dia['ejercicios']:
                    required_keys = ['nombre', 'series',
                                     'repeticiones', 'descanso']
                    if not all(key in ejercicio for key in required_keys):
                        return False

            return True
        except Exception:
            return False

    def generate_training_plan(
        self,
        experience_level: str,
        fitness_goal: str,
        available_days: int,
        health_conditions: str = None
    ) -> Dict[str, Any]:
        """
        Genera un plan de entrenamiento personalizado usando OpenAI.

        Args:
            experience_level: Nivel de experiencia (BEG, INT, ADV)
            fitness_goal: Objetivo del entrenamiento
            available_days: Días disponibles para entrenar
            health_conditions: Condiciones de salud a considerar

        Returns:
            Dict: Plan de entrenamiento estructurado

        Raises:
            ValidationError: Si la respuesta no tiene el formato esperado
        """
        prompt = self._create_prompt(
            experience_level,
            fitness_goal,
            available_days,
            health_conditions
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un entrenador personal profesional experto en crear planes de entrenamiento."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            plan = json.loads(response.choices[0].message.content)

            if not self._validate_response(plan):
                raise ValidationError(
                    "La respuesta de OpenAI no tiene el formato esperado")

            return plan

        except json.JSONDecodeError:
            raise ValidationError(
                "La respuesta de OpenAI no es un JSON válido")
        except Exception as e:
            raise ValidationError(
                f"Error al generar el plan de entrenamiento: {str(e)}")
