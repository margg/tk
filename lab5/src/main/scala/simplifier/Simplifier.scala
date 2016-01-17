package simplifier

import AST._

// to implement
// avoid one huge match of cases
// take into account non-greedy strategies to resolve cases with power laws
object Simplifier {

  def simplify(node: Node): Node = node match {

    // recognize tuples: (x,y)+(u,v) => (x, y, u, v)
    case BinExpr("+", Tuple(a), Tuple(b)) => Tuple((a ++ b) map simplify)

    // simplify if-else instruction with known condition
    case IfElseInstr(cond, left, right) =>
      val cond_simplified = simplify(cond)
      cond_simplified match {
        case TrueConst() => simplify(left)
        case FalseConst() => simplify(right)
        case _ => IfElseInstr(cond_simplified, simplify(left), simplify(right))
      }

    // simplify if-else expression with known condition
    case IfElseExpr(cond, left, right) =>
      val cond_simplified = simplify(cond)
      cond_simplified match {
        case TrueConst() => simplify(left)
        case FalseConst() => simplify(right)
        case _ => IfElseExpr(cond_simplified, simplify(left), simplify(right))
      }

    case NodeList(list) =>
      val list_simplified = list map simplify
      if (list_simplified.size == 1) list_simplified.head else NodeList(list_simplified)

    // other cases that do not change nodes
    case x => x
  }

}
