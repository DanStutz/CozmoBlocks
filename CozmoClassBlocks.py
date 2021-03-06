# import the cozmo and image libraries
import cozmo

# import libraries for movement and asynchronous behavior
import asyncio
from cozmo.util import degrees, distance_mm

# from colors import Colors
# from woc import WOC
import _thread
import time

def cozmo_program(robot: cozmo.robot.Robot):
    # turn backpack lights to RED
    # robot.set_all_backpack_lights(Colors.RED)

    # settings for signals from Cozmo's camera
    robot.camera.image_stream_enabled = True

    # initially, we may not be connected to our cubes
    cubes = None

    # connect to the cubes
    robot.world.connect_to_cubes()

    # look around and try to find a cube
    look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)

    # we can adjust this to wait until 1, 2 or 3 cubes have been observed
    cubes = robot.world.wait_until_observe_num_objects(3, object_type=cozmo.objects.LightCube, timeout=60)

    robot.say_text("I found the cubes").wait_for_completed()
    print("Found cubes: %s" % cubes)

    if cubes:
        # stop looking around
        look_around.stop()

        try:
            robot.say_text("Tap a cube so I know you are paying attention.").wait_for_completed()

            # wait for one of the cubes to be tapped
            cube_tapped = robot.wait_for(cozmo.objects.EvtObjectTapped)
        except asyncio.TimeoutError:
            robot.say_text("No one tapped a cube.").wait_for_completed()
            print("No one tapped a cube :-(")
        finally:
            if cube_tapped.obj.object_id == 1:
                robot.say_text("Block 1 was tapped.").wait_for_completed()
            elif cube_tapped.obj.object_id == 2:
                robot.say_text("Cube 2 was tapped.").wait_for_completed()
            elif cube_tapped.obj.object_id == 3:
                robot.play_anim("anim_petdetection_dog_03").wait_for_completed()

            cozmoString = "I am tired of this program."
            robot.say_text(cozmoString).wait_for_completed()

            for cube in cubes:
                cube.set_lights_off()

            return


cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)
