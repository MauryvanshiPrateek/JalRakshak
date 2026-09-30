"""
Simulation Service — orchestrates the full simulation lifecycle.

The UI interacts only with SimulationService, never with the runner directly.
This makes it easy to swap MockSimulationEngine → AnugaSimulationEngine.
"""
from __future__ import annotations
import threading
from typing import Callable, Optional

from models.scenario import Scenario
from models.simulation_result import SimulationResult, SimulationStatus
from simulation.mock_runner import MockSimulationEngine


ProgressCallback = Callable[[SimulationStatus, str, int], None]


class SimulationService:
    """
    Manages the complete lifecycle of a dam-break simulation run.

    Phase 1: Uses MockSimulationEngine.
    Phase 4+: Switch engine to AnugaSimulationEngine.
    """

    def __init__(self, engine=None):
        self._engine = engine or MockSimulationEngine()
        self._active_result: Optional[SimulationResult] = None
        self._history: list[SimulationResult] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def submit(
        self,
        scenario: Scenario,
        progress_callback: Optional[ProgressCallback] = None,
        blocking: bool = True,
    ) -> SimulationResult:
        """
        Validate and run a simulation.

        Parameters
        ----------
        scenario : Scenario
        progress_callback : callable(status, message, pct) | None
            Called at each lifecycle step to update the UI.
        blocking : bool
            If True, run synchronously (blocks until done).
            If False, run in a background thread.

        Returns
        -------
        SimulationResult (completed or in-progress).
        """
        errors = scenario.validate()
        if errors:
            result = SimulationResult(
                status=SimulationStatus.FAILED,
                status_message="Validation failed: " + "; ".join(errors),
                scenario_id=scenario.scenario_id,
            )
            return result

        result = SimulationResult(
            status=SimulationStatus.CREATED,
            status_message="Simulation created.",
            scenario_id=scenario.scenario_id,
            scenario_name=scenario.preset_name or "Custom",
        )
        self._active_result = result

        if blocking:
            self._run(scenario, result, progress_callback)
        else:
            t = threading.Thread(
                target=self._run,
                args=(scenario, result, progress_callback),
                daemon=True,
            )
            t.start()

        return result

    def get_active_result(self) -> Optional[SimulationResult]:
        return self._active_result

    def get_history(self) -> list[SimulationResult]:
        return list(reversed(self._history))

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _run(
        self,
        scenario: Scenario,
        result: SimulationResult,
        callback: Optional[ProgressCallback],
    ):
        try:
            self._engine.run(scenario, result, progress_callback=callback)
            self._history.append(result)
        except Exception as exc:
            result.status = SimulationStatus.FAILED
            result.status_message = f"Simulation error: {exc}"
            if callback:
                callback(SimulationStatus.FAILED, result.status_message, 0)
