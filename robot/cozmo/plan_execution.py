import asyncio
import cozmo
from cozmo.util import degrees, Pose
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id

# Home and Way points position
# These values depend to your real position in the environment
# Way point one
w1 = Pose(130, 145, 0, angle_z=degrees(0))
# Way point two
w2 = Pose(130, 470, 0, angle_z=degrees(0))
# Home
home = Pose(0, 0, 0, angle_z=degrees(0))
exit_home = Pose(130, 0, 0, angle_z=degrees(0))


def init_robot_world(robot: cozmo.robot.Robot):
    cube1 = robot.world.get_light_cube(LightCube1Id)
    cube2 = robot.world.get_light_cube(LightCube2Id)
    cube3 = robot.world.get_light_cube(LightCube3Id)

    cube1.set_lights(cozmo.lights.Light(cozmo.lights.Color(rgb=(220, 220, 220), name="grey")))
    cube2.set_lights(cozmo.lights.Light(cozmo.lights.Color(rgb=(220, 220, 220), name="grey")))
    cube3.set_lights(cozmo.lights.Light(cozmo.lights.Color(rgb=(204, 0, 0), name="red")))


def wait(robot: cozmo.robot.Robot):
    print("wait action execution")
    try:
        robot.say_text(text="I have to wait here").wait_for_completed(10)
        robot.play_anim(name="anim_bored_event_02").wait_for_completed(10)
    except Exception as e:
        print("ERROR: %sn" + str(e))


def mov_hw1(robot: cozmo.robot.Robot):
    print("mov_hw1 action execution")
    try:
        robot.go_to_pose(exit_home, relative_to_robot=False).wait_for_completed(20)
        robot.go_to_pose(w1, relative_to_robot=False).wait_for_completed(20)
        cube1 = robot.world.get_light_cube(LightCube1Id)
        cube1.set_lights(cozmo.lights.Light(cozmo.lights.Color(rgb=(102, 255, 102), name="green")))
        robot.say_text(text="I'm at way point one").wait_for_completed(10)
        robot.play_anim(name="anim_memorymatch_successhand_cozmo_01").wait_for_completed(10)
    except Exception as e:
        print("ERROR: %sn" + str(e))


def mov_hw2(robot: cozmo.robot.Robot):
    print("mov_hw2 action execution")
    try:
        robot.go_to_pose(exit_home, relative_to_robot=False).wait_for_completed(20)
        robot.go_to_pose(w2, relative_to_robot=False).wait_for_completed(20)
        cube2 = robot.world.get_light_cube(LightCube2Id)
        cube2.set_lights(cozmo.lights.Light(cozmo.lights.Color(rgb=(255, 255, 102), name="yellow")))
        robot.say_text(text="I'm at way point two").wait_for_completed(10)
        robot.play_anim(name="anim_memorymatch_successhand_cozmo_01").wait_for_completed(10)
    except Exception as e:
        print("ERROR: %sn" + str(e))


def mov_w1w2(robot: cozmo.robot.Robot):
    print("mov_w1w2 action execution")
    try:
        robot.go_to_pose(w2, relative_to_robot=False).wait_for_completed(20)
        cube2 = robot.world.get_light_cube(LightCube2Id)
        cube2.set_lights(cozmo.lights.Light(cozmo.lights.Color(rgb=(255, 255, 102), name="yellow")))
        robot.say_text(text="I visited way point one and now I'm in way point two").wait_for_completed(10)
        robot.play_anim(name="anim_memorymatch_successhand_cozmo_01").wait_for_completed(10)
    except Exception as e:
        print("ERROR: %sn" + str(e))


def mov_w1h(robot: cozmo.robot.Robot):
    print("mov_w1h action execution")
    try:
        robot.go_to_pose(exit_home, relative_to_robot=False).wait_for_completed(20)
        robot.go_to_pose(home, relative_to_robot=False).wait_for_completed(20)
        robot.say_text(text="I visited way point one and now I'm in my home").wait_for_completed(10)
        robot.play_anim(name="anim_memorymatch_successhand_cozmo_01").wait_for_completed(10)
    except Exception as e:
        print("ERROR: %sn" + str(e))


def mov_w2h(robot: cozmo.robot.Robot):
    print("mov_w2h action execution")
    try:
        robot.go_to_pose(exit_home, relative_to_robot=False).wait_for_completed(20)
        robot.go_to_pose(home, relative_to_robot=False).wait_for_completed(20)
        robot.say_text(text="I visited way point two and now I'm in my home").wait_for_completed(10)
        robot.play_anim(name="anim_memorymatch_successhand_cozmo_01").wait_for_completed(10)
    except Exception as e:
        print("ERROR: %sn" + str(e))


def mov_w2w1(robot: cozmo.robot.Robot):
    print("mov_w2w1 action execution")
    try:
        robot.go_to_pose(w1, relative_to_robot=False).wait_for_completed(20)
        cube1 = robot.world.get_light_cube(LightCube1Id)
        cube1.set_lights(cozmo.lights.Light(cozmo.lights.Color(rgb=(102, 255, 102), name="green")))
        robot.say_text(text="I visited way point two and now I'm in my way point one").wait_for_completed(10)
        robot.play_anim(name="anim_memorymatch_successhand_cozmo_01").wait_for_completed(10)
    except Exception as e:
        print("ERROR: %sn" + str(e))


def mov_w12h(robot: cozmo.robot.Robot):
    print("mov_w12h action execution")
    try:
        robot.go_to_pose(exit_home, relative_to_robot=False).wait_for_completed(20)
        robot.go_to_pose(home, relative_to_robot=False).wait_for_completed(20)
        robot.say_text(text="I visited way point one and two and now I'm in my home").wait_for_completed(10)
        robot.play_anim(name="anim_memorymatch_successhand_cozmo_01").wait_for_completed(10)
    except Exception as e:
        print("ERROR: %sn" + str(e))


def start(robot: cozmo.robot.Robot):
    print("start action execution")
    try:
        robot.say_text(text="I have a request to complete").wait_for_completed(10)
    except Exception as e:
        print("ERROR: %sn" + str(e))


# Actions in domain problem
action_list = {"wait": wait,
               "mov_hw1": mov_hw1,
               "mov_hw2": mov_hw2,
               "mov_w1w2": mov_w1w2,
               "mov_w1h": mov_w1h,
               "mov_w2h": mov_w2h,
               "mov_w2w1": mov_w2w1,
               "mov_w12h": mov_w12h,
               "start": start}
