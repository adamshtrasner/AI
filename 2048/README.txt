208837260
207542143
*****
Comments:
## Q5 ##
We used a sum of 2 evaluation functions minus penalties:
(1) weighted sum of board - We used a score matrix, giving each place in the board
a score according to the board's monotonicity: We found out after much research and
game plays that keeping higher tiles more clustered to the corner will result in a
better score, and so we used a snake shaped like matrix, giving higher scores as u get close
to the top left corner, and also it's reasonable to put tiles with different values in a
monotonic order so that they could merge consecutively, and so the reasoning behind the snake
shaped score matrix.
(2) uniformity evaluation - We scored states based on the sum of all numbers of tiles of the
same value, powered to 3 (after examining we thought it suits best).
This way, The chosen algorithm will choose moves that produce the most tiles of the same value.

penalty:
(1) total differences - The idea behind this is smoothness. In order for both tiles to merge
they need to have the same value, so we penalize states that that difference is high,
and the penalty for those that have low difference is low.
(2) number of empty tiles - The more empty tiles you have the more you're far away from losing,
and vice versa. Therefore, we penalized states that have less empty tiles. We powered the penalty
by 6, also after many experiments, we found that that power gives the best performance.
