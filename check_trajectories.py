import numpy as np
from robopy.robots.franka import Franka
from robopy.trajectory import LoadTrajectory
from robopy.user_interaction import press_enter
import matplotlib.pyplot as plt


def play_pouring(id):
    trajectory = LoadTrajectory("dataset/trajectory_%d.npy" % id)
    print("duration", np.sum(trajectory.duration))


if __name__ == "__main__":

    franka = Franka()
    n_demos = int(input("How many demos do you want to play? "))
    id_min = int(input("From which ID? "))

    for id in range(id_min, id_min + n_demos):
        print("STARTING DEMO %d (%d of %d)" % (id, id - id_min + 1, n_demos))
        play_pouring(id)

        trajectory = LoadTrajectory("dataset/trajectory_%d.npy" % id)

        fig, axis = plt.subplots(len(franka.groups["arm_gripper"].refs))
        trajectory.plot(axis)
        plt.savefig("dataset/traj_plot_%d.jpg" % id)


