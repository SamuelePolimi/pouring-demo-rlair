import numpy as np
from robopy.robots.franka import Franka
from robopy.hardware.scale import DymoScale, ScaleObserver
from robopy.observers import RobotObserver
from robopy.recording import Recorder, WaitingToEnd, WaitingToStart
from robopy.trajectory import GoToTrajectory, LoadTrajectory
from robopy.user_interaction import yn_question, press_enter
import time


def grasp_glass(franka: Franka):
    while True:
        franka._gripper_interface.move_joints(0.05)
        if yn_question("Is the plastic cup grasped correctly?"):
            break
        franka._gripper_interface.open()
        franka._gripper_interface.stop_action()
        print("Try to place the cup again and press ENTER")
        press_enter()


def play_pouring(id, scale_observer, franka):
    print("Press ENTER when you are ready to play the demo.")
    press_enter()

    trajectory = LoadTrajectory("dataset/trajectory_%d.npy" % id)
    recorded_weight = np.load("dataset/weight_%d.npy" % id)

    init_trajectory = trajectory.get_init_trajectory(5)
    franka.go_to(init_trajectory, "arm")
    franka.go_to(trajectory, "arm")

    time.sleep(3)
    current_weight = scale_observer("DYMO_WEIGHT")["DYMO_WEIGHT"]

    print("The current weight is: %dg" % current_weight)
    print("The saved weight was: %dg" % recorded_weight)


if __name__ == "__main__":

    franka = Franka()
    scale = DymoScale()

    observer = RobotObserver(franka)

    robot_recorder = Recorder(observer, observer.get_possible_refs(), sampling_frequency=20)
    scale_observer = ScaleObserver(scale)

    trajectory = LoadTrajectory("positions/home.npy")
    franka.go_to(trajectory, "arm")

    if yn_question("Do you need grasping the glass?"):
        franka._gripper_interface.open()
        franka._gripper_interface.stop_action()

        """
        Grasp the glass
        """

        print("""GRASPING GLASS
    
        The robot is in position for grasping the plastic cup.
        Place the plastic cup in between the grippers and press ENTER.
        """)
        press_enter()

        grasp_glass(franka)


    n_demos = int(input("How many demos do you want to play?"))
    id_min = int(input("From which ID?"))

    for id in range(id_min, id_min + n_demos):
        print("STARTING DEMO %d (%d of %d)" % (id, id - id_min + 1, n_demos))
        play_pouring(id, scale_observer, franka)
        print("When you will press ENTER, I will open the gripper. Take the cup!")
        press_enter()

        franka._gripper_interface.open()
        franka._gripper_interface.stop_action()

        time.sleep(3)
        print("Robot going in home position.")

        print("Grasping the glass when ready.")
        press_enter()
        grasp_glass(franka)



