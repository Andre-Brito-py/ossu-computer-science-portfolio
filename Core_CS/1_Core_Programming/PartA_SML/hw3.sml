(* Programming Languages Part A - SML *)
(* Pattern Matching and Type Inference Example *)

datatype pattern = Wildcard
		 | Variable of string
		 | UnitP
		 | ConstP of int
		 | TupleP of pattern list
		 | ConstructorP of string * pattern

datatype valu = Const of int
	      | Unit
	      | Tuple of valu list
	      | Constructor of string * valu

(* Returns a list of all variables in a pattern *)
fun get_variables (p : pattern) : string list =
    case p of
	Variable x => [x]
      | TupleP ps => List.foldl (fn (p', acc) => acc @ get_variables p') [] ps
      | ConstructorP (_, p') => get_variables p'
      | _ => []

(* Checks if all variables in a pattern are unique *)
fun check_pat (p : pattern) : bool =
    let
        val vars = get_variables p
        fun has_repeats [] = false
          | has_repeats (x::xs) = List.exists (fn y => x = y) xs orelse has_repeats xs
    in
        not (has_repeats vars)
    end

(* Matches a value against a pattern, returning variable bindings if successful *)
fun match (v : valu, p : pattern) =
    case (v, p) of
	(_, Wildcard) => SOME []
      | (v', Variable x) => SOME [(x, v')]
      | (Unit, UnitP) => SOME []
      | (Const c1, ConstP c2) => if c1 = c2 then SOME [] else NONE
      | (Tuple vs, TupleP ps) =>
	if length vs = length ps
	then
	    let
                val zipped = ListPair.zip (vs, ps)
                val matches = List.map match zipped
	    in
                if List.all (fn x => isSome x) matches
                then SOME (List.foldl (fn (SOME m, acc) => acc @ m) [] matches)
                else NONE
	    end
	else NONE
      | (Constructor(s1, v1), ConstructorP(s2, p1)) =>
	if s1 = s2 then match(v1, p1) else NONE
      | _ => NONE

(* Test cases *)
val p1 = TupleP [Variable "x", Variable "y"]
val v1 = Tuple [Const 1, Const 2]
val test_match = match (v1, p1) (* Should be SOME [("x", Const 1), ("y", Const 2)] *)
