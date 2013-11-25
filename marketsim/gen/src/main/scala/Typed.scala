package object Typed
{
    import AST.{BinOpSymbol, CondSymbol, DocString, QualifiedName}
    import syntax.scala.Printer.{typed => sc}
    import generator.python.{Printer => py}
    import AST.{ScPrintable, ScPyPrintable}

    abstract class Expr {
        def ty : Types.Base
    }

    abstract class ArithExpr
            extends Expr
            with    sc.Expr
            with    py.Expr
            with    ScPyPrintable

    case class Neg(x : ArithExpr)
            extends ArithExpr
            with    sc.Neg
            with    py.Neg
            with    TypeInference.Neg

    case class BinOp(symbol : BinOpSymbol,
                     x      : ArithExpr,
                     y      : ArithExpr)
            extends ArithExpr
            with    sc.BinOp
            with    py.BinOp
            with    TypeInference.BinOp

    case class IfThenElse(cond  : BooleanExpr,
                          x     : ArithExpr,
                          y     : ArithExpr)
            extends ArithExpr
            with    sc.IfThenElse
            with    py.IfThenElse
            with    TypeInference.IfThenElse

    case class FloatConst(x : Double)
            extends ArithExpr
            with    sc.FloatConst
            with    py.FloatConst
            with    TypeInference.FloatConst

    case class ParamRef(p : Parameter)
            extends ArithExpr
            with    sc.ParamRef
            with    py.ParamRef
            with    TypeInference.ParamRef

    case class FunctionCall(target      : Function,
                            arguments   : List[(Parameter, ArithExpr)])
            extends ArithExpr
            with    sc.FunCall
            with    py.FunCall
            with    TypeInference.FunctionCall

    case class Annotation(target    : AnnotationHandler,
                          parameters: List[String])
            extends sc.Annotation
            with    ScPrintable

    case class Parameter(name        : String,
                         ty          : Types.Base,
                         initializer : Option[ArithExpr],
                         comment     : List[String])
            extends sc.Parameter
            with    ScPrintable

    abstract class BooleanExpr
            extends Expr
            with    sc.BooleanExpr
            with    TypeInference.BooleanExpr

    case class Or(x : BooleanExpr,
                  y : BooleanExpr)
            extends BooleanExpr
            with    sc.Or
            with    ScPrintable

    case class And(x : BooleanExpr,
                   y : BooleanExpr)
            extends BooleanExpr
            with    sc.And
            with    ScPrintable

    case class Not(x : BooleanExpr)
            extends BooleanExpr
            with    sc.Not
            with    ScPrintable

    case class Condition(symbol : CondSymbol,
                         x      : ArithExpr,
                         y      : ArithExpr)
            extends BooleanExpr
            with    sc.Condition
            with    ScPrintable
            with    TypeInference.Condition

    case class Function(parent      : Package,
                        name        : String,
                        parameters  : List[Parameter],
                        ret_type    : Types.Base,
                        body        : Option[Expr],
                        docstring   : Option[DocString],
                        annotations : List[Annotation])
            extends sc.Function
            with    ScPrintable
    {
        parent.insert(this)

        override def equals(o : Any) = o match {
            case that : Function =>
                parent.qualifiedName == that.parent.qualifiedName &&
                name                 == that.name &&
                parameters           == that.parameters &&
                ret_type             == that.ret_type &&
                body                 == that.body &&
                docstring            == that.docstring &&
                annotations          == that.annotations
            case _ => false
        }

    }

    class Package extends sc.TopLevelPackage with ScPrintable
    {
        var functions = Map[String, Function]()
        var packages = Map[String, SubPackage]()

        def qualifiedName : List[String] = Nil

        def qualifyName(x : String) = x

        def insert(f : Function) {
            functions = functions.updated(f.name, f)
        }

        def createChild(n : String) = {
            val p = new SubPackage(n, this)
            packages = packages.updated(p.name, p)
            p
        }

        override def equals(o : Any) = o match {
            case that : Package => functions.equals(that.functions) && packages.equals(that.packages)
            case _ => false
        }

        def getOrElseUpdateFunction(name : String, default : => Typed.Function) =
            functions get name match {
                case Some(f) => f
                case None =>
                    val f = default
                    functions = functions updated (f.name, f)
                    f
            }
    }

    class SubPackage(val name : String, parent : Package) extends Package with sc.SubPackage with ScPrintable
    {
        override def qualifiedName = parent.qualifiedName :+ name

        override def qualifyName(x : String) = (qualifiedName mkString ".") + "." + x

        override def equals(o : Any) = o match {
            case that : SubPackage => super.equals(o) && name == that.name
            case _ => false
        }
    }

    trait AnnotationHandler
    {
        val name : String
    }

    object Annotations
    {
        var registry = Map[String, AnnotationHandler]()

        def register(handler : AnnotationHandler){
            registry = registry.updated(handler.name, handler)
        }

        def lookup(name : String) = registry.get(name) match {
            case Some(handler) => handler
            case None => throw new Exception(s"Cannot find annotation handler $name")
        }

        override def toString = registry.toString
    }

}
