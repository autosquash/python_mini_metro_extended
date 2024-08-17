from collections.abc import Sequence

import pygame

from src.config import Config
from src.engine.debug_renderer import DebugRenderer
from src.entity import Path
from src.gui.gui import get_gui_height

from .game_components import GameComponents
from .passenger_spawner import TravelPlansMapping
from .path_edition import EditingIntermediateStations

MAIN_SURFACE_COLOR = (180, 180, 120)


class GameRenderer:
    __slots__ = ("_components", "debug_renderer")

    def __init__(self, components: GameComponents) -> None:
        self._components = components
        self.debug_renderer = DebugRenderer(self._components)

    def render_game(
        self,
        screen: pygame.surface.Surface,
        *,
        main_surface_height: float,
        paths: Sequence[Path],
        editing_intermediate_stations: EditingIntermediateStations | None,
        travel_plans: TravelPlansMapping,
        is_creating_path: bool,
        ms_until_next_spawn: float,
        showing_debug: bool,
        game_speed: float,
    ) -> None:
        main_surface_pos = (0, get_gui_height())
        main_surface_size = (Config.screen_width, main_surface_height)
        main_surface = screen.subsurface(main_surface_pos, main_surface_size)
        main_surface.fill(MAIN_SURFACE_COLOR)
        self._draw_paths(screen, paths)
        if editing_intermediate_stations:
            editing_intermediate_stations.draw(screen)
        for station in self._components.stations:
            station.draw(screen)
        for metro in self._components.metros:
            metro.draw(screen)
        self._components.gui.render(screen, self._components.status.score)
        if showing_debug:
            self.debug_renderer.draw_debug(
                screen,
                is_creating_path,
                travel_plans,
                ms_until_next_spawn,
                game_speed,
            )

    def _draw_paths(
        self, screen: pygame.surface.Surface, paths: Sequence[Path]
    ) -> None:
        for path in paths:
            path.draw(screen)
