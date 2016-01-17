package simplifier

import AST._

// to implement
// avoid one huge match of cases
// take into account non-greedy strategies to resolve cases with power laws
object Simplifier {

  def simplify(node: Node): Node = node match {

    // recognize tuples: (x,y)+(u,v) => (x, y, u, v)
    case BinExpr("+", Tuple(a), Tuple(b)) => Tuple(a ++ b)

  }

}
