# Курсовая работа по предмету "Корягин 2.0"
#### Version 0.1.0
Реализован парсинг текста и анализ синтаксических ошибок.
## Задание
1. Написать парсер дифференциальных уравнений   
 Разделы
    1. Дифференциальные уравнения
    2. Начальные условия
    3. Метод интегрирования (3+ штук)
    4. Промежуток интегрирования, шаг
2. Реализовать систему диагностики
3. **Графики** после интегрирования
  
# Парсер дифференциальных уравнений
## Приложение
Простое приложение с графическим интерфейсом, позволяющее решать систему из простых дифференциальных уравнений. Программа считает плозади кривых на заданном интервале и рисует их графики.
### Методы интегрирования
* С постоянным шагом
    1. Эйлера
    1. Рунге-Кутты 2 порядка
    1. Рунге-Кутты 3 порядка
    1. Рунге-Кутты 4 порядка
* С плавающим шагом
    1. Рунге-Кутта-Фельберга 4-5 порядка
    1. Рунге-Кутта-Дормана-Принса 4-5 порядка
### Форма Бэкуса-Наура 
В нотации Корягина С.В.
```
Language = "Programm" ProgramName Equations BeginConditions IntegrationConfitions
ProgramName = Var
Equations = "Equations" ":" Equation ... Equation
BeginConditions = "BeginConditions" ":" BeginContition ... BeginCondition
IntegrationConfitions = "IntegrationConfitions" ":"  IntegrationConfition

Equation = IntegrationVar "=" RightBlock
RightBlock = </ "-" /> AdditionBlock ("+" ! "-") ... AdditionBlock
AdditionBlock = MultiplicationBlock ("*" ! "/") ... MultiplicationBlock 
MultiplicationBlock = Var ! Number ! "(" RightBlock ")"

BeginContition = Var "=" Number

IntegrationConfition = IntegrationConfitionMethod IntegrationConfitionPeriod IntegrationConfitionStep
IntegrationConfitionMethod = "method" "=" ("Euler" ! "Runge-Kutti-1" ! "Runge-Kutti-2" ! ... ! "Runge-Kutti-4")
IntegrationConfitionPeriod = "t" "=" Number
IntegrationConfitionStep = "dt" "=" Number

IntegrationVar = Var "/dt"
Var = Symbol ... Symbol
Symbol = Character ! Number
Number = FloatNumber ! IntNumber
IntNumber = Digit ... Digit
FloatNumber = IntNumber "." IntNumber
Character = "a" ! "b" ! ... ! "z" ! SpecialCharacter
SpecialCharacter = "_"
Digit = 0 ! 1 ! ... ! 9
```

### Пример языка

```
program DiffSolv1.0

Equations:
Susc/dt = -A * Susc * Sick
Sick/dt = A * Susk * Sick - (B + C) * Sick
Cured/dt = B * Sick

BeginConditions:
Susk = 620
Sick = 10
Cured = 70
A = 000.1
B = 0.07
C = 0.01

IntegrationConfitions:
method = Euler
t = 50
dt = 0.5

```   