208837260
207542143
*****
Comments:
## Q5 ##
We used a sum of 2 evaluation functions minus penalties:
(1) number of empty tiles - The more empty tiles you have the more 
you're far away from losing. Therefore, we scored each state with this
number - squared.
(2) weighted sum of board - We used a score matrix, giving each place in the board
a score according to the board's monotonicity: We found out after much research and
game plays that keeping higher tiles more clustered to the corner will result in a
better score, and so we used a snake shaped like matrix, giving higher scores as
u get close to the top left corner, and also it's reasonable to put tiles with
different values in a monotonic order so that they could merge consecutively,
and so the reasoning behind the snake shaped score matrix.
