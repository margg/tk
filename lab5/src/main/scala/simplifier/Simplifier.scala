package simplifier

import AST._
import scala.collection.mutable.ListBuffer

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
      case ("+", Unary("-", Variable(a)), Variable(b)) =>
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
      case ("/", IntNum(a), BinExpr("/", IntNum(b), expr)) if a == 1 && b == 1 => expr
      case ("*", expr, BinExpr("/", IntNum(a), expr2)) if a == 1 => BinExpr("/", expr, expr2)
      case ("*", BinExpr("/", IntNum(a), expr2), expr) if a == 1 => BinExpr("/", expr, expr2)

      // understand distributive property of multiplication
      case ("+", BinExpr("+", BinExpr("*", Variable(a), BinExpr("+", Variable(b), Variable(d))),
        BinExpr("*", Variable(c), Variable(b2))), BinExpr("*", Variable(c2), Variable(d2)))
        if b == b2 && c == c2 && d == d2 =>
          BinExpr("*", BinExpr("+", Variable(a), Variable(c)), BinExpr("+", Variable(b), Variable(d)))

      case (oper, BinExpr("*", a, b), BinExpr("*", c, d)) if oper == "+" || oper == "-" =>
        (a, b, c, d) match {
          case (expr_, Variable(b_), expr2_, Variable(d_)) if b_ == d_ =>
            simplify(BinExpr("*", simplify(BinExpr(oper, expr_, expr2_)), Variable(b_)))
          case (expr_, Variable(b_), Variable(c_), expr2_) if b_ == c_ =>
            simplify(BinExpr("*", simplify(BinExpr(oper, expr_, expr2_)), Variable(b_)))
          case (Variable(a_), expr_, expr2_, Variable(d_)) if a_ == d_ =>
            simplify(BinExpr("*", Variable(a_), simplify(BinExpr(oper, expr_, expr2_))))
          case (Variable(a_), expr_, Variable(c_), expr2_) if a_ == c_ =>
            simplify(BinExpr("*", Variable(a_), simplify(BinExpr(oper, expr_, expr2_))))
          case (a_, b_, c_, d_) => BinExpr(oper, simplify(BinExpr("*", a_, b_)), simplify(BinExpr("*", c_, d_)))
        }

      case (oper, Variable(a), BinExpr("*", c, d)) if oper == "+" || oper == "-" =>
        (a, c, d) match {
          case (a_, Variable(c_), expr_) if a_ == c_ =>
            simplify(BinExpr("*", Variable(a_), BinExpr(oper, IntNum(1), expr_)))
          case (a_, expr_, Variable(d_)) if a_ == d_ =>
            simplify(BinExpr("*", Variable(a_), BinExpr(oper, IntNum(1), expr_)))
          case (a_, c_, d_) => BinExpr(oper, Variable(a_), simplify(BinExpr("*", c_, d_)))
        }

      case (oper, BinExpr("*", c, d), Variable(a)) if oper == "+" || oper == "-" =>
        (c, d, a) match {
          case (Variable(c_), expr_, a_) if a_ == c_ =>
            simplify(BinExpr("*", BinExpr(oper, expr_, IntNum(1)), Variable(a_)))
          case (expr_, Variable(d_), a_) if a_ == d_ =>
            simplify(BinExpr("*", BinExpr(oper, expr_, IntNum(1)), Variable(a_)))
          case (c_, d_, a_) => BinExpr(oper, simplify(BinExpr("*", c_, d_)), Variable(a_))
        }


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

    case NodeList(list_raw) => list_raw map simplify match {
      case list if list.size == 1 => simplify(list.head)
      case list => {
        // remove dead assignments
        val buffer = ListBuffer.empty[Node]
        list.sliding(2).foreach(l => (simplify(l(0)), simplify(l(1))) match {
          case (Assignment(a1, b1), Assignment(a2, b2))
            if a1 == a2 && b2 != a2 => buffer += Assignment(a2, b2)
          case (a, b) => buffer ++ (List(a, b) map simplify)
        })
        NodeList(buffer.toList)
      }
    }

    // other cases that do not change nodes
    case x => x
  }

}
