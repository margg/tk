package simplifier

import AST._
import scala.collection.mutable.ListBuffer

// to implement
// avoid one huge match of cases
// take into account non-greedy strategies to resolve cases with power laws
object Simplifier {

  def simplify(node: Node): Node = node match {
    case BinExpr(op, left, right) => simplifyBinExpr(op, simplify(left), simplify(right))
    case IfElseInstr(cond, left, right) =>
      simplifyIfElseInstr(simplify(cond), simplify(left), simplify(right))
    case IfElseExpr(cond, left, right) =>
      simplifyIfElseExpr(simplify(cond), simplify(left), simplify(right))
    case WhileInstr(cond, body) =>
      simplifyWhileInstr(simplify(cond), simplify(body))
    case Assignment(left, right) =>
      simplifyAssignment(simplify(left), simplify(right))
    case Unary(op, expr) => simplifyUnary(op, simplify(expr))
    case KeyDatumList(list) => simplifyKeyDatumList(list)
    case NodeList(list) => simplifyNodeList(list)

    // simplify children of other node types
    case KeyDatum(key, value) => KeyDatum(simplify(key), simplify(value))
    case Tuple(list) => Tuple(list map simplify)
    case ClassDef(name, inherit_list, suite) =>
      ClassDef(name, simplify(inherit_list), simplify(suite))
    case LambdaDef(formal_args, body) =>
      LambdaDef(simplify(formal_args), simplify(body))
    case FunDef(name, formal_args, body) =>
      FunDef(name, simplify(formal_args), simplify(body))
    case FunCall(name, args_list) =>
      FunCall(simplify(name), simplify(args_list))
    case PrintInstr(expr) => PrintInstr(simplify(expr))
    case ReturnInstr(expr) => ReturnInstr(simplify(expr))
    case IfInstr(cond, left) => IfInstr(simplify(cond), simplify(left))
    case GetAttr(expr, attr) => GetAttr(simplify(expr), attr)
    case Subscription(expr, sub) => Subscription(simplify(expr), simplify(sub))

    case x => x // other cases that do not change nodes: IntNum, TrueConst, etc.
  }

  def simplifyBinExpr(op: String, left: Node, right: Node): Node = (op, left, right) match {
    // recognize tuples: (x,y)+(u,v) => (x, y, u, v)
    case ("+", Tuple(a), Tuple(b)) => Tuple((a ++ b) map simplify)
    // concatenate lists
    case ("+", ElemList(a), ElemList(b)) => ElemList((a ++ b) map simplify)

    // simplify expressions
    case ("+", a, IntNum(b)) if b == 0 => a
    case ("+", IntNum(a), b) if a == 0 => b
    case ("+", Unary("-", Variable(a)), Variable(b)) =>
      simplifyBinExpr("-", Variable(b), Variable(a))
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

    // recognize power laws
    case ("*", BinExpr("**", a1, b1), BinExpr("**", a2, b2)) if a1 == a2 =>
      BinExpr("**", a1, BinExpr("+", b1, b2))
    case ("**", BinExpr("**", a, b), c) => BinExpr("**", a, BinExpr("*", b, c))
    case ("**", a, IntNum(n)) if n == 0 => IntNum(1)
    case ("**", a, IntNum(n)) if n == 1 => a

    case ("+", BinExpr(oper, BinExpr("**", a1, IntNum(n1)), BinExpr("*", BinExpr("*", IntNum(n2), a2), b1)), BinExpr("**", b2, IntNum(n3)))
      if (n1 == 2 && n2 == 2 && n3 == 2) && ((a1 == a2 && b1 == b2) || (a1 == b1 && a2 == b2)) && (oper == "+" || oper == "-") =>
      simplify(BinExpr("**", BinExpr(oper, a1, b2), IntNum(2)))
    case (oper, BinExpr("+", BinExpr("**", a1, IntNum(n1)), BinExpr("**", b2, IntNum(n3))), BinExpr("*", BinExpr("*", IntNum(n2), a2), b1))
      if (n1 == 2 && n2 == 2 && n3 == 2) && ((a1 == a2 && b1 == b2) || (a1 == b1 && a2 == b2)) && (oper == "+" || oper == "-") =>
      simplify(BinExpr("**", BinExpr(oper, a1, b2), IntNum(2)))
    case ("+", BinExpr("+", BinExpr("*", BinExpr("*", IntNum(n2), a2), b1), BinExpr("**", a1, IntNum(n1))), BinExpr("**", b2, IntNum(n3)))
      if (n1 == 2 && n2 == 2 && n3 == 2) && ((a1 == a2 && b1 == b2) || (a1 == b1 && a2 == b2)) =>
      simplify(BinExpr("**", BinExpr("+", a1, b2), IntNum(2)))
    case ("-", BinExpr("-", BinExpr("**", BinExpr("+", a1, b1), IntNum(n1)), BinExpr("**", a2, IntNum(n2))), BinExpr("*", BinExpr("*", IntNum(n3), a3), b2))
      if (n1 == 2 && n2 == 2 && n3 == 2) && ((a1 == a2 && a1 == a3 && b1 == b2) || (a1 == a2 && a1 == b2 && b1 == a3)) =>
      simplify(BinExpr("**", b1, IntNum(2)))

    case ("-", BinExpr("**", BinExpr("+", a1, b1), IntNum(n1)), BinExpr("**", BinExpr("-", a2, b2), IntNum(n2)))
      if (n1 == 2 && n2 == 2) && ((a1 == a2 && b1 == b2) || (a1 == b2 && b1 == a2)) =>
      simplify(BinExpr("*", BinExpr("*", IntNum(4), a2), b2))

    // evaluate constants
    // integers
    case ("+", IntNum(a), IntNum(b)) => IntNum(a + b)
    case ("-", IntNum(a), IntNum(b)) => IntNum(a - b)
    case ("*", IntNum(a), IntNum(b)) => IntNum(a * b)
    case ("/", IntNum(a), IntNum(b)) => IntNum(a / b)
    case ("**", IntNum(a), IntNum(b)) => IntNum(scala.math.pow(a.intValue(), b.intValue()).toInt)
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

    // simplify division
    case ("/", Variable(a), Variable(b)) if a == b => IntNum(1)
    case ("/", BinExpr(oper, a, b), BinExpr(oper2, a2, b2))
      if (oper == oper2) && (((a == a2) && (b == b2))
        || (List("+", "*").contains(oper) && (a == b2) && (b == a2))) => IntNum(1)
    case ("/", IntNum(a), BinExpr("/", IntNum(b), expr)) if a == 1 && b == 1 => expr
    case ("*", expr, BinExpr("/", IntNum(a), expr2)) if a == 1 => BinExpr("/", expr, expr2)
    case ("*", BinExpr("/", IntNum(a), expr2), expr) if a == 1 => BinExpr("/", expr, expr2)

    // understand commutativity
    case ("and", BinExpr("or", a1, b1), BinExpr("or", a2, b2)) if (a1 == a2 && b1 == b2) || (a1 == b2 && b1 == a2) =>
      BinExpr("or", a1, b1)
    case ("or", BinExpr("and", a1, b1), BinExpr("and", a2, b2)) if (a1 == a2 && b1 == b2) || (a1 == b2 && b1 == a2) =>
      BinExpr("and", a1, b1)

    case ("-", BinExpr("+", Variable(a), expr), Variable(a1)) if a == a1 => expr // a+expr-a1
    case ("-", BinExpr("-", Variable(a), expr), Variable(a1)) if a == a1 => simplify(Unary("-", expr)) // a-expr-a1
    case ("-", BinExpr("+", expr, Variable(a)), Variable(a1)) if a == a1 => expr // expr+a-a1
    case ("+", BinExpr("-", expr, Variable(a)), Variable(a1)) if a == a1 => expr // expr-a+a1
    case ("+", BinExpr("+", Unary("-", Variable(a)), expr), Variable(a1)) if a == a1 => expr // -a + expr + a1
    case ("+", BinExpr("-", Unary("-", Variable(a)), expr), Variable(a1)) if a == a1 => simplify(Unary("-", expr)) // -a + expr + a1

    // understand distributive property of multiplication
    case ("+", BinExpr("+", BinExpr("*", a, BinExpr("+", b, d)), BinExpr("*", c, b2)), BinExpr("*", c2, d2))
      if b == b2 && c == c2 && d == d2 =>
      BinExpr("*", BinExpr("+", a, c), BinExpr("+", b, d))

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

    case (_, a, b) => BinExpr(op, a, b)
  }

  def simplifyIfElseInstr(cond: Node, left: Node, right: Node): Node = (cond, left, right) match {
    case (TrueConst(), l, r) => simplify(left)
    case (FalseConst(), l, r) => simplify(right)
    case _ => IfElseInstr(cond, left, right)
  }

  def simplifyIfElseExpr(cond: Node, left: Node, right: Node): Node = (cond, left, right) match {
    // simplify if-else expression with known condition
    case (TrueConst(), l, r) => simplify(left)
    case (FalseConst(), l, r) => simplify(right)
    case _ => IfElseExpr(cond, left, right)
  }

  def simplifyWhileInstr(cond: Node, body: Node): Node = (cond, body) match {
    case (FalseConst(), b) => NodeList(List())
    case _ => WhileInstr(cond, body)
  }

  def simplifyAssignment(left: Node, right: Node): Node = (left, right) match {
    case (Variable(a), Variable(b)) if a == b => NodeList(List())
    case (_, _) => Assignment(left, right)
  }

  def simplifyUnary(op: String, expr: Node): Node = (op, expr) match {
    // cancel double unary ops & get rid of not before comparisons
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
    case _ => Unary(op, expr)
  }

  def simplifyKeyDatumList(list: List[KeyDatum]): Node = list match {
    case _ => KeyDatumList({
      list.foldLeft(Map.empty[Node, KeyDatum])({
        (m, kd) => m + (kd.key -> kd)
      }).values.toList
    })
  }

  def simplifyNodeList(list: List[Node]): Node = list map simplify match {
    case lst if lst.size == 1 => simplify(lst.head)
    case lst =>
      // remove dead assignments
      val buffer = ListBuffer.empty[Node]
      lst.sliding(2).foreach(l => (simplify(l.head), simplify(l(1))) match {
        case (Assignment(a1, b1), Assignment(a2, b2))
          if a1 == a2 && b2 != a2 => buffer += Assignment(a2, b2)
        case (a, b) => buffer ++ (List(a, b) map simplify)
      })
      NodeList(buffer.toList)
  }

}
