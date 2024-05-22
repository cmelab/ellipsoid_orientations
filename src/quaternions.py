import numpy as np
import rowan

def rotate_quaternion(q, theta, axis):
    cos_theta_2 = np.cos(theta / 2)
    sin_theta_2 = np.sin(theta / 2)

    if axis == 'x':
        r = [cos_theta_2, sin_theta_2, 0, 0]
    elif axis == 'y':
        r = [cos_theta_2, 0, sin_theta_2, 0]
    elif axis == 'z':
        r = [cos_theta_2, 0, 0, sin_theta_2]
    else:
        raise ValueError("Axis must be 'x', 'y', or 'z'")

    q0, q1, q2, q3 = q
    r0, r1, r2, r3 = r

    q_prime = [
        r0 * q0 - r1 * q1 - r2 * q2 - r3 * q3,
        r0 * q1 + r1 * q0 + r2 * q3 - r3 * q2,
        r0 * q2 - r1 * q3 + r2 * q0 + r3 * q1,
        r0 * q3 + r1 * q2 - r2 * q1 + r3 * q0
    ]

    return rowan.normalize(q_prime)

def vector_angle(r1, r2, degree=True):
    dot = np.dot(r1, r2)
    l_r1 = np.linalg.norm(r1)
    l_r2 = np.linalg.norm(r2)
    angle = np.arccos(dot / (l_r1 * l_r2))
    if degree:
        return np.rad2deg(angle)
    return angle
    
def dr_orientation_angles(dr, q, degree=True):
    R = rowan.to_matrix(q)
    angles = []
    for i in range(3):
       angles.append(vector_angle(dr, R[:, i], degree=degree))
    return angles