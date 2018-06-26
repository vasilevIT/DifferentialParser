# Language examples

## Example 1
```
Program: DiffSolv

Equations:
Susc/dt = -A * Susc * Sick;
Sick/dt = A * Susc * Sick - (B + C) * Sick;
Cured/dt = B * Sick;

BeginConditions:
Susc = 620;
Sick = 10;
Cured = 70;
A = 0.001;
B = 0.07;
C = 0.01;

IntegrationConditions:
method = Euler;
t = 50;
dt = 0.5;
```


## Example 2
```
Program: DiffSolv

Equations:
x/dt = x - y;
y/dt = -A * x + B * y;

BeginConditions:
x = 0;
y = 5;
A = 2;
B = 3;

IntegrationConditions:
method = Euler;
t = 1.5;
dt = 0.1;
```


## Example 3
```
Program: DiffSolv

Equations:
x/dt = e ^ (2*y) + e ^ y -2;
y/dt = 2/3 * (x^2 - x)+ 3 * y - 4 * x * y;

BeginConditions:
x = 0.2;
y = 0.9;
e = 2.81;

IntegrationConditions:
method = Euler;
t = 3;
dt = 0.1;

```

## Example 4
```
Program: DiffSolv

Equations:
x/dt = (a - b*y) * x;
y/dt = (-c+s*x) * y;

BeginConditions:
a = 0.7;
b = 0.07;
s = 0.004;
c = 0.3;
x = 100;
y = 10;

IntegrationConditions:
method = Runge-Kutti-4;
t = 30;
dt = 0.1;

```


## Example 5
```
Program: DiffSolv

Equations:
x/dt = sin(x);
y/dt = cos(y);

BeginConditions:
x = 0.0001;
y = 0.0001;

IntegrationConditions:
method = Euler;
t = 50;
dt = 0.5;

```

## Example 6
```
Program: DiffSolv

Equations:
x/dt = sin((x/0.2)*2);
y/dt = cos(y * x + 2);

BeginConditions:
x = 0.0001;
y = 0.0001;

IntegrationConditions:
method = Euler;
t = 50;
dt = 0.5;
```