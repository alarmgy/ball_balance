import math
import scipy as sp

d = 0.04

W_THETA = 1
W_PHI = 1
W_L = 0.3

def l(l1, l2, l3):
    return (1/3) * (l1 + l2 + l3)

def phi(l1, l2, l3):
    return math.atan2(math.sqrt(3) * (l2 + l3 - 2*l1),
                      3 * (l2 - l3))

def kappa(l1, l2, l3):
    x = l1**2 + l2**2 + l3**2 - l1*l2 - l1*l3 - l2*l3
    if abs(x) < 1e-18:
        x = 1e-18
    return ((2 * math.sqrt(x)) /
            (d * (l1 + l2 + l3)))

def theta(l1, l2, l3):
    return l(l1, l2, l3) * kappa(l1, l2, l3)

def cost(x, theta_desired, phi_desired, prev_l):
    l1, l2, l3 = x[0], x[1], x[2]

    dl1 = (l1 - prev_l[0])
    dl2 = (l2 - prev_l[1])
    dl3 = (l3 - prev_l[2])

    ret = (W_THETA * (theta(l1, l2, l3) - theta_desired)**2 + W_PHI * (phi(l1, l2, l3) - phi_desired)**2 +
               W_L * (dl1**2 + dl2**2 + dl3**2))

    # print(theta_desired, theta(l1, l2, l3), ret)

    return ret

def IK(Ox, Oy, prev_l):
    Ox = math.radians(Ox)
    Oy = math.radians(Oy)

    theta_desired = math.sqrt(pow(Ox, 2) + pow(Oy, 2))
    phi_desired = math.atan2(-Ox, Oy)

    l = [0.04, 0.03, 0.035]
    bounds = [(0.02, 0.05) for i in range(3)]
    
    res = sp.optimize.minimize(cost, l, args=(theta_desired, phi_desired, prev_l), bounds=bounds) 

    # print(res)
    return res.x
