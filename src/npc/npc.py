from __future__ import annotations

from typing import Callable

import pygame

from src.enums import FarmingTool, InventoryResource, Layer, StudyGroup
from src.gui.interface.emotes import NPCEmoteManager
from src.npc.bases.npc_base import NPCBase
from src.npc.behaviour.npc_behaviour_tree import NPCIndividualContext
from src.overlay.soil import SoilManager
from src.settings import Coordinate
from src.sprites.entities.character import Character
from src.sprites.setup import EntityAsset


class NPC(NPCBase):
    def __init__(
        self,
        pos: Coordinate,
        assets: EntityAsset,
        groups: tuple[pygame.sprite.Group, ...],
        collision_sprites: pygame.sprite.Group,
        study_group: StudyGroup,
        apply_tool: Callable[[FarmingTool, tuple[float, float], Character], None],
        plant_collision: Callable[[Character], None],
        soil_manager: SoilManager,
        emote_manager: NPCEmoteManager,
        tree_sprites: pygame.sprite.Group,
    ):
        self.emote_manager = emote_manager

        self.tree_sprites = tree_sprites

        super().__init__(
            pos=pos,
            assets=assets,
            groups=groups,
            collision_sprites=collision_sprites,
            study_group=study_group,
            apply_tool=apply_tool,
            plant_collision=plant_collision,
            behaviour_tree_context=NPCIndividualContext(self),
            z=Layer.MAIN,
        )

        self.soil_area = soil_manager.get_area(self.study_group)

        # TODO: Ensure that the NPC always has all needed seeds it needs
        #  in its inventory
        self.inventory = {
            InventoryResource.WOOD: 0,
            InventoryResource.APPLE: 0,
            InventoryResource.ORANGE: 0,
            InventoryResource.PEACH: 0,
            InventoryResource.PEAR: 0,
            InventoryResource.CORN: 0,
            InventoryResource.TOMATO: 0,
            InventoryResource.CORN_SEED: 999,
            InventoryResource.TOMATO_SEED: 999,
        }

    def update(self, dt):
        super().update(dt)

        self.emote_manager.update_obj(
            self, (self.rect.centerx - 47, self.rect.centery - 128)
        )
