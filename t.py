import numpy as np

C = 0.041
h = 1.0
x0, y0 = 0, 15
xf, yf = 20, 10

def f(x, Y):
    y1, y2 = Y
    dy1dx = y2
    dy2dx = C * np.sqrt(1 + y2**2)
    return np.array([dy1dx, dy2dx])

def rk4_step(x, Y, h):
    k1 = f(x, Y)
    k2 = f(x + h/2, Y + h*k1/2)
    k3 = f(x + h/2, Y + h*k2/2)
    k4 = f(x + h, Y + h*k3)
    return Y + (h/6)*(k1 + 2*k2 + 2*k3 + k4)

def shoot(s, h):
    x = x0
    Y = np.array([y0, s])
    while x < xf:
        Y = rk4_step(x, Y, h)
        x += h
    return Y[0]  # valor de y1(xf)

# Método da secante
s0, s1 = -1.0, 0.0
y0f = shoot(s0, h)
y1f = shoot(s1, h)

for _ in range(10):
    s2 = s1 - (y1f - yf) * (s1 - s0) / (y1f - y0f)
    y2f = shoot(s2, h)
    if abs(y2f - yf) < 1e-4:
        break
    s0, y0f = s1, y1f
    s1, y1f = s2, y2f

print(f"Melhor chute s ≈ {s2:.5f}, y(20) ≈ {y2f:.5f}")