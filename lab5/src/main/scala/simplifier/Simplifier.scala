package simplifier

import AST._

// to implement
// avoid one huge match of cases
// take into account non-greedy strategies to resolve cases with power laws
object Simplifier {

  def simplify(node: Node): Node = node match {

    // recognize tuples: (x,y)+(u,v) => (x, y, u, v)
    case BinExpr("+", Tuple(a), Tuple(b)) => Tuple((a ++ b) map simplify)

    // concatenate lists
    case BinExpr("+", ElemList(a), ElemList(b)) => ElemList((a ++ b) map simplify)

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

    // remove no effect instructions
    case Assignment(left, right) => (left, right) match {
      case (Variable(a), Variable(b)) if a == b => NodeList(List())
      case (_, _) => Assignment(simplify(left), simplify(right))
    }

    // simplify expressions
    // todo: divide into smaller and cleaner match cases
    case BinExpr(op, left, right) => (op, simplify(left), simplify(right)) match {
      case ("+", a, IntNum(b)) if b == 0 => a
      case ("+", IntNum(a), b) if a == 0 => b
      case ("+", Unary("-", Variable(a)), Variable(b))=>
        simplify(BinExpr("-", Variable(b), Variable(a)))
      case ("*", Variable(x), IntNum(b)) if b == 1 => Variable(x)
      case ("*", IntNum(a), Variable(x)) if a == 1 => Variable(x)
      case ("*", Variable(x), IntNum(b)) if b == 0 => IntNum(0)
      case ("*", IntNum(a), Variable(x)) if a == 0 => IntNum(0)
      case ("-", IntNum(a), IntNum(b)) if a == b => IntNum(0)
      case ("-", Variable(a), Variable(b)) if a == b => IntNum(0)
      case ("or", a, b) if a == b => a
      case ("or", Variable(x), TrueConst()) => TrueConst()
      case ("or", Variable(x), FalseConst()) => Variable(x)
      case ("and", a, b) if a == b => a
      case ("and", Variable(x), FalseConst()) => FalseConst()
      case ("and", Variable(x), TrueConst()) => Variable(x)
      case ("==", Variable(a), Variable(b)) if a == b => TrueConst()
      case (">=", Variable(a), Variable(b)) if a == b => TrueConst()
      case ("<=", Variable(a), Variable(b)) if a == b => TrueConst()
      case ("!=", Variable(a), Variable(b)) if a == b => FalseConst()
      case ("<", Variable(a), Variable(b)) if a == b => FalseConst()
      case (">", Variable(a), Variable(b)) if a == b => FalseConst()

      // integers
      case ("+", IntNum(a), IntNum(b)) => IntNum(a + b)
      case ("-", IntNum(a), IntNum(b)) => IntNum(a - b)
      case ("*", IntNum(a), IntNum(b)) => IntNum(a * b)
      case ("/", IntNum(a), IntNum(b)) => IntNum(a / b)
      case ("**", IntNum(a), IntNum(b)) => IntNum(a ^ b)
      case ("<", IntNum(a), IntNum(b)) => if (a < b) TrueConst() else FalseConst()
      case ("<=", IntNum(a), IntNum(b)) => if (a <= b) TrueConst() else FalseConst()
      case (">", IntNum(a), IntNum(b)) => if (a > b) TrueConst() else FalseConst()
      case (">=", IntNum(a), IntNum(b)) => if (a >= b) TrueConst() else FalseConst()
      case ("==", IntNum(a), IntNum(b)) => if (a == b) TrueConst() else FalseConst()
      case ("!=", IntNum(a), IntNum(b)) => if (a != b) TrueConst() else FalseConst()

      // floats
      case ("+", FloatNum(a), FloatNum(b)) => FloatNum(a + b)
      case ("-", FloatNum(a), FloatNum(b)) => FloatNum(a - b)
      case ("*", FloatNum(a), FloatNum(b)) => FloatNum(a * b)
      case ("/", FloatNum(a), FloatNum(b)) => FloatNum(a / b)
      case ("<", FloatNum(a), FloatNum(b)) => if (a < b) TrueConst() else FalseConst()
      case ("<=", FloatNum(a), FloatNum(b)) => if (a <= b) TrueConst() else FalseConst()
      case (">", FloatNum(a), FloatNum(b)) => if (a > b) TrueConst() else FalseConst()
      case (">=", FloatNum(a), FloatNum(b)) => if (a >= b) TrueConst() else FalseConst()
      case ("==", FloatNum(a), FloatNum(b)) => if (a == b) TrueConst() else FalseConst()
      case ("!=", FloatNum(a), FloatNum(b)) => if (a != b) TrueConst() else FalseConst()

      // simplifying division
      case ("/", Variable(a), Variable(b)) if a == b => IntNum(1)
      case ("/", BinExpr(oper, a, b), BinExpr(oper2, a2, b2))
        if (oper == oper2) && (((a == a2) && (b == b2))
          || (List("+", "*").contains(oper) && (a == b2) && (b == a2))) => IntNum(1)
      case ("/", IntNum(a), BinExpr("/", IntNum(b), expr)) if a == 1 && b == 1 => expr    // simplify(expr)?
      case ("*", expr, BinExpr("/", IntNum(a), expr2)) if a == 1 => BinExpr("/", expr, expr2)
      case ("*", BinExpr("/", IntNum(a), expr2), expr) if a == 1 => BinExpr("/", expr, expr2)

      case (_, a, b) => BinExpr(op, simplify(a), simplify(b))
    }

    // cancel double unary ops & get rid of not before comparisons
    case Unary(op, expr) => (op, simplify(expr)) match {
      case ("not", TrueConst()) => FalseConst()
      case ("not", FalseConst()) => TrueConst()
      case ("not", Unary("not", expr1)) => simplify(expr1)
      case ("not", BinExpr("==", left, right)) => simplify(BinExpr("!=", left, right))
      case ("not", BinExpr("!=", left, right)) => simplify(BinExpr("==", left, right))
      case ("not", BinExpr(">", left, right)) => simplify(BinExpr("<=", left, right))
      case ("not", BinExpr("<", left, right)) => simplify(BinExpr(">=", left, right))
      case ("not", BinExpr(">=", left, right)) => simplify(BinExpr("<", left, right))
      case ("not", BinExpr("<=", left, right)) => simplify(BinExpr(">", left, right))
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
