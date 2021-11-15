# prefix_evaluator
Recursively evaluate prefix expressions using Python

## Usage
```bash
% python3 prefixeval.py input.txt 
> (* 2 15)
30
> (+  (* 12 4)(* 2 3 ))
54
> (-  (* 12 2)(* 2 3 ))
18
> (* 5 (/ 5 2))
10
> (or (> 6 13) (< 15 2))
False
> (and (> 13 6) (> 17 3))
True
> (or (and (> 13 25) (< 6 5)) (and (> 14 2) (< 31 65)))
True
> (+  1 (* 12 4)(weird 3 2))
49
> (+  1 (* 12 4 )(* 2 2)
Missing closing ')'
> (/ (+ 3 5))
Incorrect number of operands - must be 2 for '/'
> (+ (- 4 2 3) 8))
Incorrect number of operands - must be 2 for '-'
> (* (+ 3 X) 5)
Expected int found: 'X'
> +
None
> (+  1 * 12 4)(* 3 2))
Expected int found: '*'
> (+  1 (* 12 4)(* 2 3 ))
49
```
