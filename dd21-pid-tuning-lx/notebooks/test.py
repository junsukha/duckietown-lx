import sys

# TODO: modify <yourGitHubName> to make this the path to your exercise folder
EXERCISE_DIRECTORY = "/code/dd21-pid-tuning-lx/packages/project-pid-implementation-junsukha/"
GAINS_PATH = EXERCISE_DIRECTORY + "z_pid.yaml"

sys.path.append(EXERCISE_DIRECTORY)

from utils.writer import load_gains, update_gains

from drone_sim import VerticalDrone
from IPython.display import display

def update(height_setpoint,kp,kd,ki,k,drag_coeff=0,latency=0,noise=0):
    from student_pid_class import PID

    update_gains(kp=kp,kd=kd,ki=ki,k=k,filepath=GAINS_PATH)

    pid_gains = load_gains(GAINS_PATH)

    my_pid_instance = PID(
    kp=pid_gains['Kp'],
    kd=pid_gains['Kd'],
    ki=pid_gains['Ki'],
    k=pid_gains['K'],
    )

    sim = VerticalDrone(
                    pid_controller=my_pid_instance,
                    # step_size=10,
                    drag_coeff=drag_coeff,
                    latency=latency,
                    sensor_noise=noise,
                    mass=0.7 # mass in kg
                    )

    sim.update_setpoint(height=height_setpoint)
    sim.simulate(end_time=15.0)
    sim.plot_step_response()



import ipywidgets as widgets
# from ipywidget import *

kp_widget = widgets.FloatSlider(value=1.0,description='Kp',max=2.0,min=0.0)
kd_widget = widgets.FloatSlider(description='Kd',value=1.0, max=2.0,min=0.0)
ki_widget = widgets.FloatSlider(description='Ki',value=1.0, max=2.0,min=0.0)

k_widget = widgets.BoundedFloatText(value=1000,max=1900,min=900,description='K')
height_setpoint=widgets.FloatSlider(value=0.5,min=0.0,max=1.0,description="Setpoint")

ui = widgets.HBox(
    [
        widgets.VBox([kp_widget,kd_widget,ki_widget,k_widget]),
        widgets.VBox(
            [   
                height_setpoint,
                # drag_coeff,
                # latency,
                # noise,
            ]
        )
    ]
    )

out = widgets.interactive_output(
    update,
    {
        'height_setpoint': height_setpoint,
        # 'drag_coeff' : drag_coeff,
        # 'latency' : latency,
        # 'noise' : noise,
        'kp' : kp_widget,
        'kd' : kd_widget,
        'ki' : ki_widget,
        'k'  : k_widget
    }
    )

display(ui,out)