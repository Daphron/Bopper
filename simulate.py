import math
from Box2D import *
from Box2D.b2 import *
import pygame
from pygame.locals import *
import Caveman as cm
import numpy as np
import sys

def endgame(screen):
    for i in range(480):
        pygame.draw.line(screen, (255,0,0), (0,i), (640,0))
        pygame.draw.line(screen, (255,0,0), (0,480), (640, 480-i))
        pygame.display.flip()
        pygame.time.wait(1)

    sys.exit()

def create_caveman(world, x_pos, caveman):
    mbody = world.CreateDynamicBody(position=(x_pos, cm.HEIGHT/2))
    mbody_density = caveman.wBody / 2 *(1 * cm.HEIGHT/2)
    box = mbody.CreatePolygonFixture(box=(1, cm.HEIGHT/2), density=mbody_density , friction=0.3)
    box.filterData.groupIndex = -x_pos

    a1, a2 = caveman.appendages

    bicep_body = world.CreateDynamicBody(position=(x_pos+a1.lBicep/2, caveman.arm_height), angle=pi/2)
    bicep_density = a1.wBicep / 2*(0.5 * a1.lBicep)
    bicep = bicep_body.CreatePolygonFixture(box=(0.5, a1.lBicep/2), density=bicep_density, friction=0.3)
    bicep.filterData.groupIndex = -x_pos
    joint1 = world.CreateRevoluteJoint(bodyA=mbody, bodyB=bicep_body, localAnchorA=(0,caveman.arm_height - cm.HEIGHT/2.0) , localAnchorB=(0, a1.lBicep/2), lowerAngle = -pi, upperAngle = pi, enableMotor=True)

    forearm_width = 0.5
    forearm_body = world.CreateDynamicBody(position=(x_pos+a1.lBicep, caveman.arm_height), angle=pi/2)
    forearm_density = a1.wForearm / 2*(0.5 * a1.lForearm)
    forearm = forearm_body.CreatePolygonFixture(box=(0.5, a1.lForearm/2), density=forearm_density, friction=0.3)
    forearm.filterData.groupIndex = -x_pos

    joint2=world.CreateRevoluteJoint(bodyA=bicep_body, bodyB=forearm_body, localAnchorA=(0, -a1.lBicep/2), localAnchorB=(0, a1.lForearm/2), lowerAngle=-pi, upperAngle = pi)

    bopper_radius = a1.rBopper
    bopper_body = world.CreateDynamicBody(position=(x_pos+a1.lBicep+a1.lForearm, caveman.arm_height), angle=0)
    bopper_density = a1.wBopper / pi*(a1.rBopper)**2
    bopper = bopper_body.CreateCircleFixture(radius=bopper_radius, density=bopper_density, friction=0.3)
    joint3=world.CreateRevoluteJoint(bodyA=forearm_body, bodyB=bopper_body, localAnchorA=(0, -a1.lForearm/2), localAnchorB=(0,0), lowerAngle=-pi, upperAngle=pi)

    bicep2_body2 = world.CreateDynamicBody(position=(x_pos-a2.lBicep/2, caveman.arm_height), angle= -pi/2)
    bicep2_density2 = a2.wBicep / 2*(0.5 * a2.lBicep)
    bicep2 = bicep2_body2.CreatePolygonFixture(box=(0.5, a2.lBicep/2), density=bicep2_density2, friction=0.3)
    bicep2.filterData.groupIndex = -x_pos
    joint12 = world.CreateRevoluteJoint(bodyA=mbody, bodyB=bicep2_body2, localAnchorA=(0,caveman.arm_height - cm.HEIGHT/2.0) , localAnchorB=(0, a2.lBicep/2), lowerAngle = -pi, upperAngle = pi, enableMotor=True)

    forearm_width2 = 0.5
    forearm_body2 = world.CreateDynamicBody(position=(x_pos-a2.lBicep, caveman.arm_height), angle= -pi/2)
    forearm_density2 = a2.wForearm / 2*(0.5 * a2.lForearm)
    forearm2= forearm_body2.CreatePolygonFixture(box=(0.5, a2.lForearm/2), density=forearm_density2, friction=0.3)
    forearm2.filterData.groupIndex = -x_pos

    joint22=world.CreateRevoluteJoint(bodyA=bicep2_body2, bodyB=forearm_body2, localAnchorA=(0, -a2.lBicep/2), localAnchorB=(0, a2.lForearm/2), lowerAngle=-pi, upperAngle = pi)

    bopper_radius2 = a2.rBopper
    bopper_body2 = world.CreateDynamicBody(position=(x_pos-a2.lBicep-a2.lForearm, caveman.arm_height), angle=0)
    bopper_density2 = a2.wBopper / pi*(a2.rBopper)**2
    bopper2 = bopper_body2.CreateCircleFixture(radius=bopper_radius2, density=bopper_density2, friction=0.3)
    joint3=world.CreateRevoluteJoint(bodyA=forearm_body2, bodyB=bopper_body2, localAnchorA=(0, -a2.lForearm/2), localAnchorB=(0,0), lowerAngle=-pi, upperAngle=pi)

    return ([mbody, bicep_body, forearm_body, bopper_body, joint1, joint2], [mbody, bicep2_body2, forearm_body2, bopper_body2, joint12, joint22])

def simulate(caveman1, caveman2, graphics_enabled=False):

    PPM = 20.0 # pixels per meter
    FPS = 60
    SCREEN_WIDTH, SCREEN_HEIGHT=640,480
    
    if graphics_enabled:
        screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), 0, 32)
        pygame.display.set_caption("Bopper")
    clock = pygame.time.Clock()


    world = b2World()
    groundBody=world.CreateStaticBody(
            userData="ground",
            position=(0, -9),
            shapes=b2PolygonShape(box=(50,10)))

    bodies1_1, bodies1_2 = create_caveman(world,15, caveman1)
    mbody = bodies1_1[0]
    joint1_1 = bodies1_1[-2:]
    bodies1_1 = bodies1_1[:-2]
    joint1_2 = bodies1_2[-2:]
    bodies1_2 = bodies1_2[:-2]
    bodies2_1, bodies2_2 = create_caveman(world, 22, caveman2)
    mbody2 = bodies2_1[0]
    bodies2_1 = bodies2_1[:-2]
    joint2_1 = bodies2_1[-2:]
    bodies2_2 = bodies2_2[:-2]
    joint2_2 = bodies2_2[-2:]
    all_bodies = bodies1_1 + bodies2_1 + [groundBody] + bodies1_2 + bodies2_2

    boppers = [bodies1_1[3], bodies2_1[3], bodies1_2[3], bodies2_2[3]]
    bodies1_1 = bodies1_1[:-1]
    bodies2_1 = bodies2_1[:-1]
    bodies1_2 = bodies1_2[:-1]
    bodies2_2 = bodies2_2[:-1]

    game_over_bodies1 = bodies1_1 + bodies1_2
    game_over_bodies2 = bodies2_1 + bodies2_2
    
    timeStep = 1.0 / FPS
    vel_iters = 6
    pos_iters = 2

    total_time = 0
    time_param = 0

    running = True
    while running:
        time_param += 1

        if graphics_enabled:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        import pdb; pdb.set_trace()


        # import pdb; pdb.set_trace()
        # np.polynomial.polynomial.polyval(1, caveman1.appendages[0].iElbow)
        # Motors for first arm of first robot
        joint1_1[0].maxMotorTorque = 1000
        joint1_1[0].motorSpeed =1* np.polynomial.polynomial.polyval(time_param % 50, caveman1.appendages[1].iShoulder)
        joint1_1[1].motorSpeed = 1*np.polynomial.polynomial.polyval(time_param % 50, caveman1.appendages[1].iElbow)

        #Motors for first arm of 2nd robot
        joint2_1[0].maxMotorTorque = 1000
        joint2_1[0].motorSpeed = 1*np.polynomial.polynomial.polyval(time_param % 50, caveman1.appendages[1].iShoulder)
        joint2_1[1].motorSpeed = 1*np.polynomial.polynomial.polyval(time_param % 50, caveman1.appendages[1].iElbow)

        # Motors for second arm of first robot
        joint1_2[0].maxMotorTorque = 1000
        joint1_2[0].motorSpeed = 1*np.polynomial.polynomial.polyval(time_param % 50, caveman1.appendages[1].iShoulder)
        joint1_2[1].motorSpeed = 1*np.polynomial.polynomial.polyval(time_param % 50, caveman1.appendages[1].iElbow)

        #Motors for second arm of 2nd robot
        joint2_2[0].maxMotorTorque = 1000
        joint2_2[0].motorSpeed = 1*np.polynomial.polynomial.polyval(time_param % 50, caveman1.appendages[1].iShoulder)
        joint2_2[1].motorSpeed = 1*np.polynomial.polynomial.polyval(time_param % 50, caveman1.appendages[1].iElbow)

        # print np.polynomial.polynomial.polyval(clock.get_time()*100, caveman1.appendages[0].iElbow)

        if graphics_enabled:
            screen.fill((0,0,0,0))
            for body in all_bodies:
                for fixture in body.fixtures:
                    shape = fixture.shape
                    if body not in boppers:
                        vertices = [(body.transform*v)*PPM for v in shape.vertices]
                        vertices = [(v[0], SCREEN_HEIGHT-v[1]) for v in vertices]

                        if body == groundBody:
                            pygame.draw.polygon(screen, (0,255,0,255), vertices)
                        else:
                            pygame.draw.polygon(screen, (255,255,255,255), vertices)

                    else:
                        pygame_radius = fixture.shape.radius * PPM
                        pygame_loc = (int(body.position[0] * PPM), int(SCREEN_HEIGHT - body.position[1]*PPM))
                        pygame.draw.circle(screen, (255,0,0,255), pygame_loc, int(pygame_radius))

        world.Step(timeStep, vel_iters, pos_iters)
        if graphics_enabled:
            pygame.display.flip()
        total_time += clock.get_time()
        clock.tick(FPS)

        for b in game_over_bodies1:
            for contact in b.contacts:
                if contact.other.userData == 'ground':
                    if b is not mbody and b is not mbody2:
                        print "Player 1 loses"
                        endgame(screen)
                        return caveman2
                    if b is mbody and mbody.worldCenter[1] < 2.03:
                        print "Player 1 loses"
                        endgame(screen)
                        return caveman2

        for b in game_over_bodies2:
            for contact in b.contacts:
                if contact.other.userData == 'ground':
                    if b is not mbody and b is not mbody2:
                        print "Player 2 loses"
                        endgame(screen)
                        return caveman1
                        # import pdb; pdb.set_trace()
                    if b is mbody2 and mbody2.worldCenter[1] < 2.03:
                        print "Player 2 loses"
                        endgame(screen)
                        return caveman1
                        # import pdb; pdb.set_trace()

        if total_time > 15000:
            print "Draw, result returned is:"
            if mbody.worldCenter[1] > mbody2.worldCenter[1]:
                print "Player 1 wins"
                return caveman1
            else:
                print "Player 2 wins"
                return caveman2

if __name__ == "__main__":
    # simulate(cm.Caveman(2), cm.Caveman(2), True)
    d1 = [3.3896, 4.31, 3.918, 0.8, -0.2, -0.2, 0.4545, 0.25559, 4.5407, 2.338, 1.1, -0.1, -0.1, 0.802, 1.078]

    d2 = [3.01377018739, 3.66504329677, 1.97987312894,1.0,0.0,0.0,0.875262112062,1.34504116574,2.15438389199,3.65191957239,0.7,-0.1,-0.1,1.24504116574,0.953222219151]

    #Some decent punching on d3s
    d3 = [0.467912015772,3.9311662513,2.27233056981,1.0,-0.2,-0.2,0.417486832644,0.934392107919,2.69954231781,3.39529010059,1.1,-0.2,-0.2,0.309095217574,0.557879769671]

    # More opposite punching
    d4 = [3.28965624916,4.31061225347,3.91820060486,0.8,-0.2,-0.2,0.454519404991,0.255939162984,4.54071250914,2.33839279826,1.0,0.0,0.0,0.802588997549,1.2787341147]

    d24 = [0.667912015772,3.9311662513,2.27233056981,1.1,-0.2,-0.2,0.417486832644,0.834392107919,2.69954231781,3.39529010059,1.1,-0.1,-0.1,0.309095217574,0.557879769671] 

    d24_2 = [1.59682686758,2.71373821671,3.69401336818,1.2,-0.2,-0.2,0.945144209351,0.145492005134,4.16812874768,3.92849763778,0.9,-0.1,-0.1,0.545492005134,0.0530008254587]

    d28 = [1.49682686758,2.71373821671,3.79401336818,1.2,-0.3,-0.3,0.845144209351,0.245492005134,4.16812874768,3.92849763778,0.8,-0.2,-0.2,0.445492005134,0.0530008254587]
    # A true fighter!
    d28_2 = [3.25512403219,4.88115886648,2.42137971308,1.2,-0.4,-0.4,1.28832906119,0.721678758389,4.64021360659,2.74066230966,0.8,0.0,0.0,0.721678758389,0.235965100056]

    #Also a two sided beast
    d30 = [3.25512403219,4.88115886648,2.42137971308,1.2,-0.4,-0.4,1.28832906119,0.721678758389,4.64021360659,2.84066230966,0.9,0.0,0.0,0.721678758389,0.235965100056]

    d30_2 = [0.667912015772,3.9311662513,2.27233056981,1.1,0.0,0.0,0.417486832644,0.834392107919,2.69954231781,3.29529010059,1.1,-0.1,-0.1,0.409095217574,0.557879769671]

    d33 = [3.11377018739,3.36504329677,1.87987312894,1.0,0.0,0.0,0.875262112062,1.34504116574,2.25438389199,3.85191957239,0.6,-0.3,-0.3,1.24504116574,0.953222219151]

    d35 = [0.667912015772,3.8311662513,2.47233056981,1.1,0.1,0.1,0.517486832644,0.834392107919,2.69954231781,3.19529010059,1.1,0.0,0.0,0.409095217574,0.457879769671]
    
    simulate(cm.Caveman(2, d35), cm.Caveman(2, d35), True)


# ---------wBody 2.20165163625
# Arm 0
# lForearm 2.88295791734
# lBicep 3.40864718005
# rBopper 1.0
# lString -0.2
# wForearm -0.2
# wBicep 0.116777618587
# wBopper 1.04048793756
# Arm 1
# lForearm 2.31288711624
# lBicep 2.86346940852
# rBopper 1.2
# lString -0.1
# wForearm -0.1
# wBicep 0.345243435256
# wBopper 0.823579610493

