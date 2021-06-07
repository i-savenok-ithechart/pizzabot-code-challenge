# pizzabot-code-challenge
## How to execute:

- Using build script:
  >sudo bash ./pizzabot.sh [argument]
  
  *The script uses Docker to run image (and also build if it doesn't exist)
so Docker must be installed (https://docs.docker.com/get-docker/)


- Through src/pizzabot.py:

  > python src/pizzabot.py [argument]

  *Python 3.8 must be installed (https://www.python.org/downloads/release/python-382/)


- Tests:

  > pytest src
  
  *Python 3.8 and pytest must be installed.

## Input argument format:
  The argument must be provided in the next format (including quotes):
  >"{x0}x{y0} ({x1}, {y1}) ({x2}, {y..."

  where:  
  {x1}, {y1} - field height and width (integers);  
  {x1,2,3...}, {y1,2,3...} - houses in need of pizza coordinates (integers);  
  
  example:
    
  >sudo bash ./pizzabot.sh "5x5 (0, 0) (1, 3) (4,4) (4, 2) (4, 2) (0, 1)
(3, 2) (2, 3) (4, 1)"
  