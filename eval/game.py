from typing import List, Optional, Union
from diambra.arena import (
    SpaceTypes,
    EnvironmentSettingsMultiAgent,
    make,
    RecordingSettings,
)
import os
import datetime

from agent import Robot, KEN_RED, KEN_GREEN


class Game:
    render: Optional[bool] = False
    splash_screen: Optional[bool] = False
    save_game: Optional[bool] = False
    characters: Optional[List[str]] = ["Ken", "Ken"]
    outfits: Optional[List[int]] = [1, 3]
    frame_shape: Optional[List[int]] = [0, 0, 0]
    seed: Optional[int] = 42
    settings: EnvironmentSettingsMultiAgent = None  # Settings of the game
    env = None  # Environment of the game
    agent_1: Robot = None  # First agent
    agent_2: Robot = None  # Second agent

    def __init__(
        self,
        render: bool = False,
        save_game: bool = False,
        splash_screen: bool = False,
        characters: List[str] = ["Ken", "Ken"],
        outfits: List[int] = [1, 3],
        frame_shape: List[int] = [0, 0, 0],
        seed: int = 42,
    ):
        """_summary_

        Args:
            render (bool, optional): Renders the fights. Defaults to False.
            splash_screen (bool, optional): Display the splash screen. Defaults to False.
            characters (List[str], optional): List of the players to have. Defaults to ["Ryu", "Ken"].
            outfits (List[int], optional): Outfits to run. Defaults to [2, 2].
            frame_shape (List[int], optional): Don't know :D . Defaults to [0, 0, 0].
            seed (int, optional): Random seed. Defaults to 42.
        """
        self.render = render
        self.splash_screen = splash_screen
        self.save_game = save_game
        self.characters = characters
        self.outfits = outfits
        self.frame_shape = frame_shape
        self.seed = seed
        self.settings = self._init_settings()
        self.env = self._init_env(self.settings)
        self.observation, self.info = self.env.reset(seed=self.seed)

    def _init_settings(self) -> EnvironmentSettingsMultiAgent:
        """
        Initializes the settings for the game.
        """
        settings = EnvironmentSettingsMultiAgent(
            render_mode="rgb_array",
            splash_screen=self.splash_screen,
        )

        settings.action_space = (SpaceTypes.DISCRETE, SpaceTypes.DISCRETE)

        settings.characters = self.characters

        settings.outfits = self.outfits

        settings.frame_shape = self.frame_shape

        return settings

    def _init_recorder(self) -> RecordingSettings:
        """
        Initializes the recorder for the game.
        """
        if not self.save_game:
            return None
        # Recording settings in root directory
        root_dir = os.path.dirname(os.path.abspath(__file__))
        game_id = "sfiii3n"
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        recording_settings = RecordingSettings()
        recording_settings.dataset_path = os.path.join(
            root_dir, "diambra/episode_recording", game_id, "-", timestamp
        )
        recording_settings.username = "llm-colosseum"

        return recording_settings

    def _init_env(self, settings: EnvironmentSettingsMultiAgent):
        """
        Initializes the environment for the game.
        """
        render_mode = "human" if self.render else "rgb_array"
        recorder_settings = self._init_recorder()
        if self.save_game:
            return make(
                "sfiii3n",
                settings,
                render_mode=render_mode,
                episode_recording_settings=recorder_settings,
            )
        return make("sfiii3n", settings, render_mode=render_mode)

    def _save(self):
        """
        Save the game state.
        """
        pass

    def run(self):
        """
        Runs the game with the given settings.
        """

        self.agent_1 = Robot(
            action_space=self.env.action_space["agent_0"],
            character="Ken",
            side=0,
            character_color=KEN_RED,
            ennemy_color=KEN_GREEN,
        )

        self.agent_2 = Robot(
            action_space=self.env.action_space["agent_1"],
            character="Ken",
            side=1,
            character_color=KEN_GREEN,
            ennemy_color=KEN_RED,
        )

        self.agent_1.observe(self.observation, {})
        self.agent_2.observe(self.observation, {})

        while True:
            if self.render:
                self.env.render()

            # Plan
            self.agent_1.plan()
            self.agent_2.plan()

            # Act
            actions = {"agent_0": self.agent_1.act(), "agent_1": self.agent_2.act()}
            print("Actions: {}".format(actions))
            # Execute actions in the game
            observation, reward, terminated, truncated, info = self.env.step(actions)

            done = terminated or truncated
            print("Reward: {}".format(reward))
            print("Done: {}".format(done))
            print("Info: {}".format(info))

            if done:
                # Optionally, change episode settings here
                options = {}
                options["characters"] = (None, None)
                options["char_outfits"] = (5, 5)
                observation, info = self.env.reset(options=options)
                break

            # Observe the environment
            self.agent_1.observe(observation, actions)
            self.agent_2.observe(observation, actions)
        self.env.close()
        return 0
