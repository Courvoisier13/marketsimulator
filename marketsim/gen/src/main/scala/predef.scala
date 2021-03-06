package object predef {

    def pars(s : Any, condition : Boolean = true) =
        if (condition) "(" + s + ")" else s.toString

    def ifSome[A](p : Option[A], prefix : String = "", postfix : String = "") =
        if (p.nonEmpty) prefix + p.get + postfix else ""

    class Indent() {
        var x : Int = 0
        var spaces = Map[Int, String]()

        def get = at(x)

        def at(i : Int) = {
            if (!(spaces contains i)) {
                spaces = spaces updated (i, " " * i)
            }
            spaces(i)
        }

        def apply(increment : Int = 4)(f : => Any) = {
            x += increment
            val e = f.toString
            x -= increment
            e
        }

        def apply(f : => Any) : String = apply()("\r\n" + get + f)
    }

    val indent = new Indent()

    def crlf = "\r\n" + indent.get



    abstract class Code
    {
        def toString : String

        def imports : Stream[Importable] = Nil.toStream

        def ||| (t : Code) : Code = new Combine(this, t)
        def |   (t : Code) : Code = this ||| nl ||| t
        def |>  (t : Code) : Code = this ||| new Block(t)
    }

    trait Importable extends Code {
        def repr: String
    }

    case class Import(what: String) extends Code with Importable {
        override def imports = Stream(this)
        override def toString = ""
        def repr = s"import $what"
    }
    case class ImportFrom(what: String, from: String) extends Code with Importable {
        override def imports = Stream(this)
        override def toString = ""
        def repr = s"from $from import $what"
    }

    object Code
    {
        def from(lst : List[Code], sep : Code = nl) : Code = lst match {
            case Nil => stop
            case x :: Nil => x
            case x :: tl => new Combine(new Combine(x, sep), from(tl, sep))
        }
    }

    class NewLine extends Code
    {
        override def toString = crlf
    }

    class Stop extends Code
    {
        override def toString = ""
    }

    class Block(inner : Code) extends Code
    {
        override def toString = indent(inner)

        override def imports = inner.imports
    }

    class WithoutImports(inner : => Code) extends Code
    {
        override def toString = inner.toString
    }

    val nl = new NewLine
    val stop = new Stop

    class Combine(x : Code, y : Code) extends Code
    {
        override def toString = x.toString + y.toString

        override def imports = x.imports ++ y.imports
    }

    class LazyString(s : => String) extends Code {

        override def toString = s
    }

    implicit def toLazy(s : => String) = new LazyString(s)
}

