import json
from typing import Dict, Any
from openai import OpenAI
from django.conf import settings
from django.core.exceptions import ValidationError


class OpenAIService:
    def __init__(self):
        print(
            f"OpenAI Service initialized with key starting with: {settings.OPENAI_API_KEY[:7]}")
        try:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            print("DEBUG: OpenAI client initialized successfully")
        except Exception as e:
            print(f"DEBUG: Error initializing OpenAI client: {str(e)}")
            raise

        self.model = "gpt-3.5-turbo"
        self.temperature = 0.7

    def _create_prompt(self, experience_level: str, fitness_goal: str,
                       available_days: int, health_conditions: str = None) -> str:
        """Crea el prompt para OpenAI"""

        # Configuraciones según el objetivo
        training_configs = {
            "STRENGTH": {
                "reps": "4-8 repeticiones",
                "rest": "120-180 segundos",
                "description": "Enfoque en fuerza máxima"
            },
            "HYPERTROPHY": {
                "reps": "8-12 repeticiones",
                "rest": "60-90 segundos",
                "description": "Enfoque en crecimiento muscular"
            },
            "ENDURANCE": {
                "reps": "12-20 repeticiones",
                "rest": "30-45 segundos",
                "description": "Enfoque en resistencia muscular"
            },
            "WEIGHT_LOSS": {
                "reps": "12-15 repeticiones",
                "rest": "45-60 segundos",
                "description": "Enfoque en pérdida de grasa"
            }
        }

        config = training_configs.get(fitness_goal, training_configs["STRENGTH"])
        
        # Distribuciones óptimas de días
        day_distributions = {
            2: ["Lunes", "Jueves"],
            3: ["Lunes", "Miércoles", "Viernes"],
            4: ["Lunes", "Martes", "Jueves", "Viernes"],
            5: ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"],
            6: ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"],
            7: ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        }

        suggested_days = day_distributions.get(available_days, [f"Día {i+1}" for i in range(available_days)])
        days_string = ", ".join(suggested_days)

        base_prompt = f"""Actúa como un entrenador personal profesional experto en crear planes de entrenamiento.

        IMPORTANTE: DEBES DEVOLVER SOLO UN JSON VÁLIDO CON LA SIGUIENTE ESTRUCTURA.
        NO INCLUYAS NINGÚN TEXTO ADICIONAL, SOLO EL JSON.

        {{
            "dias": [
                {{
                    "dia": "Lunes",
                    "ejercicios": [
                        {{
                            "nombre": "Press de banca",
                            "series": 4,
                            "repeticiones": "6-8",
                            "descanso": "120"
                        }},
                        {{
                            "nombre": "Sentadillas",
                            "series": 4,
                            "repeticiones": "6-8",
                            "descanso": "120"
                        }}
                    ]
                }}
            ]
        }}

        INSTRUCCIONES:
        - Usar estos días exactamente: {days_string}
        - Objetivo: {config['description']}
        - Nivel: {experience_level}
        - Mínimo 4 ejercicios por día
        - Series: 3-5 (número entero)
        - Repeticiones: {config['reps']}
        - Descansos: {config['rest']}
        - Ejercicios compuestos: descansos más largos
        - Ejercicios aislados: descansos más cortos
        {f'- Considerar: {health_conditions}' if health_conditions else ''}

        RECUERDA: DEVOLVER SOLO EL JSON, SIN NINGÚN TEXTO ADICIONAL"""

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
                    # Validar tipos de datos
                    if not isinstance(ejercicio['series'], int):
                        return False
                    if not all(isinstance(ejercicio[key], str) for key in ['nombre', 'repeticiones', 'descanso']):
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
        print("DEBUG: Intentando conexión con OpenAI")
        # Para ver qué endpoint está usando
        print(f"DEBUG: URL de la API: {self.client.base_url}")
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
