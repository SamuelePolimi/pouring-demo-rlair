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


def recording(robot_recorder, scale_observer):
    robot_recorder.record_fixed_duration(15.)
    time.sleep(2)
    return robot_recorder.trajectory, scale_observer("DYMO_WEIGHT")["DYMO_WEIGHT"]


def record_puring(robot_recorder, scale_observer):
    print("Press ENTER when you are ready to start the demo.")
    press_enter()

    while True:
        trajectory, weight = recording(robot_recorder, scale_observer)
        print("The weight is: %dg" % weight)

        if yn_question("Are you satisfied with the demo?"):
            break

    return trajectory, weight


if __name__ == "__main__":

    franka = Franka()
    scale = DymoScale()

    observer = RobotObserver(franka)

    robot_recorder = Recorder(observer, observer.get_possible_refs(), sampling_frequency=20)
    scale_observer = ScaleObserver(scale)

    trajectory = LoadTrajectory("positions/home.npy")
    franka.go_to(trajectory, "arm")

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

    print("SET THE ROBOT IN TEACHING MODE PLEASE!")
    print("Press ENTER when you are done.")
    press_enter()

    n_demos = int(input("How many demos do you want to collect?"))
    id_min = int(input("From which ID do you want to save?"))

    for id in range(id_min, id_min + n_demos):
        print("STARTING DEMO %d (%d of %d)" % (id, id - id_min + 1, n_demos))
        trajectory, weight = record_puring(robot_recorder, scale_observer)
        trajectory.save("dataset/trajectory_%d.npy" % id)
        np.save("dataset/weight_%d.npy" % id, weight)
        print("DEMO SAVED")

        print("Bring robot in position.")
        press_enter()
        print("Refill the glass.")
        press_enter()

