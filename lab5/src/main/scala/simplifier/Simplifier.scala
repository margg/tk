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

    // remove while loop with False condition
    case WhileInstr(cond, body) =>
      val cond_simplified = simplify(cond)
      cond_simplified match {
        case FalseConst() => NodeList(List())
        case _ => WhileInstr(cond_simplified, simplify(body))
      }

    // simplify expressions
    case BinExpr("+", left, right) => (simplify(left), simplify(right)) match {
      case (a, IntNum(b)) if b == 0 => a
      case (IntNum(a), b) if a == 0 => b
      case (Unary("-", Variable(a)), Variable(b)) =>
        simplify(BinExpr("-", Variable(b), Variable(a)))
      case (a, b) => BinExpr("+", simplify(a), simplify(b))
    }

    case BinExpr("-", left, right) => (simplify(left), simplify(right)) match {
      case (IntNum(a), IntNum(b)) if a == b => IntNum(0)
      case (a, b) => BinExpr("+", simplify(a), simplify(b))
    }

    case BinExpr(op, left, right) => (op, simplify(left), simplify(right)) match {
      case (_, a, b) => BinExpr(op, a, b)
    }

    // cancel double unary ops & get rid of not before comparisons
    case Unary(op, expr) => (op, simplify(expr)) match {
      case ("not", Unary("not", expr1)) => simplify(expr1)
      case ("not", BinExpr("==", left, right)) =>
        simplify(BinExpr("!=", left, right))
      case ("not", BinExpr("!=", left, right)) =>
        simplify(BinExpr("==", left, right))
      case ("not", BinExpr(">", left, right)) =>
        simplify(BinExpr("<=", left, right))
      case ("not", BinExpr("<", left, right)) =>
        simplify(BinExpr(">=", left, right))
      case ("not", BinExpr(">=", left, right)) =>
        simplify(BinExpr("<", left, right))
      case ("not", BinExpr("<=", left, right)) =>
        simplify(BinExpr(">", left, right))
      case ("-", Unary("-", expr1)) => simplify(expr1)
      case (_, expr1) => Unary(op, simplify(expr1))
    }

    case NodeList(list) =>
      val list_simplified = list map simplify
      if (list_simplified.size == 1) list_simplified.head else NodeList(list_simplified)

    // other cases that do not change nodes
    case x => x
  }

}
