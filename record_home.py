import numpy as np
from robopy.robots.franka import Franka, FrankaHome
from robopy.hardware.scale import DymoScale, ScaleObserver
from robopy.observers import RobotObserver
from robopy.recording import Recorder, WaitingToEnd, WaitingToStart
from robopy.trajectory import GoToTrajectory
from robopy.user_interaction import yn_question, press_enter
import time


if __name__ == "__main__":

    franka = Franka()

    observer = RobotObserver(franka)
    observation = observer(*observer.get_possible_refs())
    print(observation)
    trajectory = GoToTrajectory(duration=5., **observation)
    trajectory.save("positions/home.npy")
