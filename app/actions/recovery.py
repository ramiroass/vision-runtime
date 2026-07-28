from typing import Dict, Any, List, Callable

class RecoveryEngine:
    def execute_with_recovery(self, strategies: List[Callable[[], Dict[str, Any]]]) -> Dict[str, Any]:
        """Intenta ejecutar una secuencia de estrategias de fallback hasta lograr el éxito."""
        attempts = []
        for index, strategy in enumerate(strategies, start=1):
            try:
                res = strategy()
                attempts.append({"attempt": index, "success": res.get("success", False), "result": res})
                if res.get("success", False):
                    return {
                        "success": True,
                        "strategy_index": index,
                        "attempts_count": len(attempts),
                        "result": res
                    }
            except Exception as e:
                attempts.append({"attempt": index, "success": False, "error": str(e)})

        return {
            "success": False,
            "strategy_index": None,
            "attempts_count": len(attempts),
            "reason": "Todas las estrategias de recuperación de fallback fallaron.",
            "attempts_log": attempts
        }

recovery_engine = RecoveryEngine()
