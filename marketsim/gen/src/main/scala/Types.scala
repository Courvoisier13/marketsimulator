package object Types
{
    import AST.ScPyPrintable
    import syntax.scala.Printer.{types => sc}
    import generator.python.Printer.{types => py}

    // TODO:
    //  Declaration     type P
    //  Typedef         type A = B
    //  Inheritance     type C : A, B
    //  Generics        type G[T] : F[T]

    sealed abstract class Base
            extends sc.Base
            with    py.Base
            with    ScPyPrintable

    case object `Float`
            extends Base
            with    sc.`Float`
            with    py.`Float`

    case object `Boolean`
            extends Base
            with    sc.`Boolean`
            with    py.`Boolean`

    case object Unit
            extends Base
            with    sc.Unit
            with    py.Unit

    case class Tuple(elems : List[Base])
            extends Base
            with    sc.Tuple
            with    py.Tuple

    case class Function(args : List[Base], ret : Base)
            extends Base
            with    sc.Function
            with    py.Function

    abstract class UserDefined
            extends Base
            with    sc.UserDefined
            with    py.UserDefined
    {
        val name : String
        val scope : Typed.Package
    }

    case class Interface(name : String, scope : Typed.Package, bases : List[Base]) extends UserDefined

    case class Declaration[T <: UserDefined](t : T)

    def nullaryFunction(ret_type : Base) = Function(List(), ret_type)
    val FloatFunc = nullaryFunction(`Float`)
    val BooleanFunc = nullaryFunction(`Boolean`)

    def fromAST(t : AST.Type) : Base = t match {
        case AST.SimpleType("Float") => `Float`
        case AST.SimpleType("Boolean") => `Boolean`
        case AST.SimpleType(name) => throw new Exception(s"Unknown type $name")
        case AST.UnitType => Unit
        case AST.TupleType(types) => Tuple(types map fromAST)
        case AST.FunctionType(arg_types, ret_type) => Function(arg_types map fromAST, fromAST(ret_type))
    }
}
