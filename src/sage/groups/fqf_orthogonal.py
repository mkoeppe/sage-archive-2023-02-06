r"""
Orthogonal Groups of Torsion Quadratic Forms

The orthogonal group of a torsion quadratic module `T`
consists of all linear self-maps of `T` which preserve
the torsion quadratic form.


EXAMPLES::

    sage: L = IntegralLattice("A2").twist(2)
    sage: T = L.discriminant_group()
    sage: Oq = T.orthogonal_group()

The isometries act on elements of their domain::

    sage: g = Oq(matrix(ZZ, 2, [0, 3, 1, 2]))
    sage: T.gen(0) * g
    (0, 3)

Isometries are represented with respect to
the Smith form generators of `T`::

    sage: L = IntegralLattice("A2").twist(2).direct_sum(IntegralLattice('U'))
    sage: T = L.discriminant_group().normal_form()
    sage: OT = T.orthogonal_group()
    sage: g = matrix(2, 2, [1, 3, 1, 2])
    sage: g = OT(g)
    sage: g
    [1 3]
    [1 2]
    sage: sf = T.smith_form_gens()
    sage: matrix([s * g for s in T.smith_form_gens()])
    [1 3]
    [1 2]

AUTHORS:

- Simon Brandhorst (2020-01-08): initial version
"""

# ****************************************************************************
#       Copyright (C) 2020 Simon Brandhorst <sbrandhorst@web.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ****************************************************************************
from sage.libs.gap.libgap import libgap
from sage.groups.abelian_gps.abelian_aut import AbelianGroupAutomorphismGroup_subgroup, AbelianGroupAutomorphism, AbelianGroupAutomorphismGroup_gap
from sage.modules.torsion_quadratic_module import TorsionQuadraticModule
from sage.rings.integer_ring import ZZ
from sage.matrix.constructor import matrix
from sage.categories.action import Action


class FqfIsometry(AbelianGroupAutomorphism):
    r"""
    Isometry of a finite quadratic/bilinear form.

    INPUT:

    - ``parent`` -- the parent :class:`~FqfOrthogonalGroup`
    - ``x`` -- a libgap element
    - ``check`` -- bool (default: ``True``)

    EXAMPLES::

            sage: q = matrix.diagonal([2/3])
            sage: q = TorsionQuadraticForm(q)
            sage: G = q.orthogonal_group()
            sage: g = G(matrix(ZZ, 1, [2]))
            sage: g
            [2]
    """

    def _repr_(self):
        r"""
        Return the string representation of ``self``.

        EXAMPLES::

            sage: q = matrix.diagonal([2/3, 4/3])
            sage: q = TorsionQuadraticForm(q)
            sage: G = q.orthogonal_group()
            sage: g = G.one()
            sage: g
            [1 0]
            [0 1]
        """
        return str(self.matrix())

    def __call__(self, x):
        r"""
        Return the image of ``x`` under ``self``.

        EXAMPLES::

            sage: q = matrix.diagonal([2/3, 4/3])
            sage: q = TorsionQuadraticForm(q)
            sage: G = q.orthogonal_group()
            sage: g = G(matrix(ZZ, 2, [1, 0, 0, 2]))
            sage: g
            [1 0]
            [0 2]
            sage: x = q.0
            sage: g(x)
            (1, 0)
        """
        if x in self.parent().invariant_form():
            return x * self
        else:
            return AbelianGroupAutomorphism.__call__(self, x)


class FqfOrthogonalGroup(AbelianGroupAutomorphismGroup_subgroup):
    r"""
    Return a group of isometries of this torsion quadratic form.

    Do not call this class directly instead use
    :meth:`sage.modules.torsion_quadratic_module.orthogonal_group`.

    INPUT:

    - ``T`` -- a non degenerate torsion quadratic module.

    EXAMPLES::

        sage: q = matrix.diagonal(QQ, [2/3, 2/3, 4/3])
        sage: T = TorsionQuadraticForm(q)
        sage: T
        Finite quadratic module over Integer Ring with invariants (3, 3, 3)
        Gram matrix of the quadratic form with values in Q/2Z:
        [2/3   0   0]
        [  0 2/3   0]
        [  0   0 4/3]
        sage: T.orthogonal_group()
        Group of isometries of
        Finite quadratic module over Integer Ring with invariants (3, 3, 3)
        Gram matrix of the quadratic form with values in Q/2Z:
        [2/3   0   0]
        [  0 2/3   0]
        [  0   0 4/3]
        generated by 3 elements
        sage: q = matrix.diagonal(QQ, [3/2, 1/4, 1/4])
        sage: T = TorsionQuadraticForm(q)
        sage: T.orthogonal_group().order()
        8

    Action on an invariant subquotient::

        sage: T = TorsionQuadraticForm(matrix.diagonal([2/9] + [2/27]))
        sage: S1 = 3 * T
        sage: S2 = 9 * T
        sage: Q = S1/S2
        sage: G = T.orthogonal_group()
        sage: g = G(matrix(ZZ, 2, [8, 0, 0, 1]))
        sage: Q.1 * g
        (0, 1)
    """
    Element = FqfIsometry

    def __init__(self, ambient, gens, fqf, check=False):
        r"""
        TESTS::

            sage: q = matrix.diagonal(QQ, [2/3, 2/3, 4/3])
            sage: T = TorsionQuadraticForm(q)
            sage: Oq = T.orthogonal_group()
            sage: TestSuite(Oq).run()
        """
        # We act on the smith form generators
        # because they are independent
        if not isinstance(fqf, TorsionQuadraticModule):
            raise TypeError("input must be a torsion quadratic module")
        if not isinstance(ambient, AbelianGroupAutomorphismGroup_gap):
            raise TypeError("input must be a torsion quadratic module")
        if not fqf.invariants() == ambient.domain().gens_orders():
            raise ValueError("invariants of the abelian groups do not match")
        gens = [ambient(g) for g in gens]
        self._invariant_form = fqf
        AbelianGroupAutomorphismGroup_subgroup.__init__(self, ambient, gens)
        if check and any(not self._preserves_form(g) for g in self.gens()):
            raise ValueError("a generator does not preserve the quadratic form")

    def invariant_form(self):
        r"""
        Return the torsion quadratic form left invariant.

        EXAMPLES::

            sage: q = matrix.diagonal(QQ, [2/3])
            sage: T = TorsionQuadraticForm(q)
            sage: Oq = T.orthogonal_group()
            sage: Oq.invariant_form() is T
            True
        """
        return self._invariant_form

    def _element_constructor_(self, x, check=True):
        r"""
        Construct an element from ``x`` and handle conversions.

        INPUT:

        - ``x`` -- something that converts in can be:

          * a libgap element
          * an integer matrix in the covering matrix ring
          * a class:`sage.modules.fg_pid.fgp_morphism.FGP_Morphism`
            defining an automorphism -- the domain of ``x`` must have
            invariants equal to ``self.domain().gens_orders()``
          * something that acts on the invariant form module

        EXAMPLES::

            sage: L = IntegralLattice("A2").twist(2).direct_sum(IntegralLattice("A2"))
            sage: q = L.discriminant_group()
            sage: OL = L.orthogonal_group()
            sage: Oq = q.orthogonal_group()
            sage: f = matrix(ZZ, 2, [0, 1, -1, -1])
            sage: f = matrix.block_diagonal([f, f])
            sage: f = OL(f)
            sage: fbar = Oq(f)
            sage: fbar
            [1 3]
            [3 4]

        Note that the following does not work since it may lead to ambiguities, see :trac:`30669`::

            sage: Oq(f.matrix())
            Traceback (most recent call last):
            ...
            ValueError: ...

        But a matrix in the covering works::

            sage: fbar == Oq(fbar.matrix())
            True

        TESTS::

            sage: all(x*f==x*fbar for x in q.gens())
            True
            sage: L = IntegralLattice("A2").twist(3)
            sage: q = L.discriminant_group()
            sage: OL = L.orthogonal_group()
            sage: Oq = q.orthogonal_group()
            sage: assert Oq(OL.0) == Oq(OL.0.matrix())
            sage: assert Oq(Oq.0.matrix()) == Oq.0
        """
        from sage.libs.gap.element import GapElement
        if not isinstance(x, GapElement):
            try:
                # if there is an action try that
                gen = self.invariant_form().smith_form_gens()
                x = matrix(ZZ, [(g*x).vector() for g in gen])
            except TypeError:
                pass
        f = AbelianGroupAutomorphismGroup_subgroup._element_constructor_(self, x, check=True)
        if check:
            # double check that the form is preserved
            # this is expensive
            if not self._preserves_form(f):
                raise ValueError("not an isometry")
        return f

    def _preserves_form(self, f):
        r"""
        Return if ``f`` preserves the form.

        INPUT:

        Something that acts on the domain.

        EXAMPLES::

            sage: T = TorsionQuadraticForm(matrix([1/4]))
            sage: G = T.orthogonal_group()
            sage: g = G.gen(0)
            sage: G._preserves_form(g)
            True
        """
        g = self.invariant_form().smith_form_gens()
        gf = tuple(h*f for h in g)
        n = len(g)
        for i in range(n):
            if gf[i].q() != g[i].q():
                return False
            for j in range(i+1, n):
                if g[i].b(g[j]) != gf[i].b(gf[j]):
                    return False
        return True

    def _get_action_(self, S, op, self_on_left):
        r"""
        Provide the coercion system with an action.

        EXAMPLES::

            sage: q = matrix.diagonal([2/3, 4/3])
            sage: q = TorsionQuadraticForm(q)
            sage: G = q.orthogonal_group()
            sage: G._get_action_(q, operator.mul, False)
            Right action by Group of isometries of
            Finite quadratic module over Integer Ring with invariants (3, 3)
            Gram matrix of the quadratic form with values in Q/2Z:
            [2/3   0]
            [  0 4/3]
            generated by 2 elements on Finite quadratic module over Integer Ring with invariants (3, 3)
            Gram matrix of the quadratic form with values in Q/2Z:
            [2/3   0]
            [  0 4/3]
        """
        import operator
        if op == operator.mul and not self_on_left:
            T = self.invariant_form()
            if S == T:
                return ActionOnFqf(self, S)
            try:
                if S.is_submodule(T):
                    # check if the submodule is invariant
                    if all(T(s)*g in S for s in S.gens() for g in self.gens()):
                        return ActionOnFqf(self, S, on_subquotient=True)
                elif S.V().is_submodule(T.V()) and T.W().is_submodule(S.W()):   # is a subquotient
                    Q1 = S.V()/T.W()
                    Q2 = S.W()/T.W()
                    if (
                        all(T(q) * g in Q1 for q in Q1.gens() for g in self.gens()) and
                        all(T(q) * g in Q2 for q in Q2.gens() for g in self.gens())
                    ):
                        return ActionOnFqf(self, S, on_subquotient=True)
            except AttributeError:
                pass
            try:
                return AbelianGroupAutomorphismGroup_subgroup._get_action_(self, S, op, self_on_left)
            except AttributeError:
                pass

    def _subgroup_constructor(self, libgap_subgroup):
        r"""
        Create a subgroup from the input.

        See :class:`~sage.groups.libgap_wrapper`. Override this in derived
        classes.

        EXAMPLES::

            sage: q = TorsionQuadraticForm(matrix.diagonal([2/3, 2/3]))
            sage: G = q.orthogonal_group()
            sage: G.subgroup(G.gens()[:1])  # indirect doctest
            Group of isometries of
            Finite quadratic module over Integer Ring with invariants (3, 3)
            Gram matrix of the quadratic form with values in Q/2Z:
            [2/3   0]
            [  0 2/3]
            generated by 1 elements
        """
        generators = libgap_subgroup.GeneratorsOfGroup()
        generators = tuple(self(g, check=False) for g in generators)
        return FqfOrthogonalGroup(self, generators, self.invariant_form(), check=False)

    def _repr_(self):
        r"""
        The string representation of ``self``.

        EXAMPLES::

            sage: q = TorsionQuadraticForm(matrix.diagonal([2/3,2/3]))
            sage: q.orthogonal_group()
            Group of isometries of
            Finite quadratic module over Integer Ring with invariants (3, 3)
            Gram matrix of the quadratic form with values in Q/2Z:
            [2/3   0]
            [  0 2/3]
            generated by 2 elements
        """
        return "Group of isometries of \n%s\ngenerated by %s elements"%(self.invariant_form(), len(self.gens()))

class ActionOnFqf(Action):
    r"""
    Action on a finite quadratic module.

    INPUT:

    - ``orthogonal_grp`` --  an instance of :class:`GroupOfIsometries`
    - ``fqf`` -- a torsion quadratic module
    - ``on_subquotient`` -- bool (default: ``False``)
    - ``is_left`` -- bool (default: ``False``)

    EXAMPLES::

        sage: q = matrix.diagonal([2/3, 4/3])
        sage: q = TorsionQuadraticForm(q)
        sage: G = q.orthogonal_group()
        sage: g = G(matrix.diagonal([2, 2]))
        sage: g
        [2 0]
        [0 2]
        sage: x = q.0
        sage: x * g
        (2, 0)
    """
    def __init__(self, orthogonal_grp, fqf, on_subquotient=False, is_left=False):
        r"""
        Initialize the action

        TESTS::

            sage: from sage.groups.fqf_orthogonal import ActionOnFqf
            sage: q = matrix.diagonal([2/3, 4/3])
            sage: q = TorsionQuadraticForm(q)
            sage: G = q.orthogonal_group()
            sage: A = ActionOnFqf(G, q, is_left=True)
            Traceback (most recent call last):
            ...
            ValueError: the action is from the right
        """
        import operator
        self._on_subquotient = on_subquotient
        if is_left:
            raise ValueError("the action is from the right")
        Action.__init__(self, orthogonal_grp, fqf, is_left, operator.mul)

    def _act_(self, g, a):
        r"""
        This defines the group action.

        INPUT:

        - ``a`` -- an element of the invariant submodule
        - ``g`` -- an element of the acting group

        OUTPUT:

        - an element of the invariant submodule

        EXAMPLES::

            sage: from sage.groups.fqf_orthogonal import ActionOnFqf
            sage: q = matrix.diagonal([2/3, 4/3])
            sage: q = TorsionQuadraticForm(q)
            sage: g1 = 2 * matrix.identity(2)
            sage: g2 = matrix(ZZ, 2, [1, 0, 0, 2])
            sage: G = q.orthogonal_group(gens=[g1, g2])
            sage: A = ActionOnFqf(G, q)
            sage: A
            Right action by Group of isometries of
            Finite quadratic module over Integer Ring with invariants (3, 3)
            Gram matrix of the quadratic form with values in Q/2Z:
            [2/3   0]
            [  0 4/3]
            generated by 2 elements on Finite quadratic module over Integer Ring with invariants (3, 3)
            Gram matrix of the quadratic form with values in Q/2Z:
            [2/3   0]
            [  0 4/3]
            sage: x = q.an_element()
            sage: g = G.an_element()
            sage: A(x, g).parent()
            Finite quadratic module over Integer Ring with invariants (3, 3)
            Gram matrix of the quadratic form with values in Q/2Z:
            [2/3   0]
            [  0 4/3]
            sage: q = TorsionQuadraticForm(matrix.diagonal([2/3, 2/3, 6/8, 1/4]))
            sage: G = q.orthogonal_group()
            sage: q2 = q.primary_part(2)
            sage: g = G(matrix.diagonal([1, 7]))
            sage: q2.gen(1) * g
            (0, 3)
        """
        if self.is_left():
            pass
            # this would be a left action but... we do not allow it.
            # v = (a.vector()*g.matrix().inverse())
            # P = a.parent()
            # return P.linear_combination_of_smith_form_gens(v)
        elif self._on_subquotient:
            S = a.parent()
            T = g.parent().invariant_form()
            return S(T(a)*g)
        else:
            v = (a.vector()*g.matrix())
            P = a.parent()
            return P.linear_combination_of_smith_form_gens(v)

def _isom_fqf(A, B=None):
    r"""
    Return isometries from `A` to `B`.

    INPUT:

    - ``A`` -- a torsion quadratic module
    - ``B`` -- (default: ``None``) a torsion quadratic module

    OUTPUT:

    A list of generators of the orthogonal group of A.
    If ``B`` is given returns instead a single isometry of `A` and `B` or
    raises an ``ValueError`` if `A` and `B` are not isometric.

    EXAMPLES::

        sage: q = matrix.diagonal(QQ, 3*[2/3])
        sage: q = TorsionQuadraticForm(q)
        sage: gens = sage.groups.fqf_orthogonal._isom_fqf(q, q)
        sage: q1 = q.submodule_with_gens(gens)
        sage: q1.gram_matrix_quadratic() == q.gram_matrix_quadratic()
        True

    TESTS::

        sage: for p in primes_first_n(7)[1:]: # long time
        ....:     q = matrix.diagonal(QQ, 3 * [2/p]) # long time
        ....:     q = TorsionQuadraticForm(q) # long time
        ....:     assert q.orthogonal_group().order()==GO(3, p).order() # long time
    """
    def orbits(G, L):
        r"""
        Return the orbits of `L` under `G`.

        INPUT:

        - ``G`` -- an fqf_orthognal group
        - ``L`` -- a list of tuples of elements of the domain of ``G``

        A list of orbit representatives of `L`
        """
        D = G.invariant_form()
        A = G.domain()
        L = libgap([[A(g).gap() for g in f] for f in L])
        orb = G.gap().Orbits(L,libgap.OnTuples)
        orb = [g[0] for g in orb]
        orb = [[D.linear_combination_of_smith_form_gens(A(g).exponents()) for g in f] for f in orb]
        return orb

    if B is None:
        B = A
        automorphisms = True
    else:
        automorphisms = False
    if A.invariants() != B.invariants():
        raise ValueError("torsion quadratic modules are not isometric")
    n = len(A.smith_form_gens())
    # separating the different primes here would speed things up
    b_cand = [[b for b in B if b.q()==a.q() and b.order() == a.order()] for a in A.smith_form_gens()]

    G = B.orthogonal_group(tuple())
    ambient = G.ambient()
    waiting = [[]]
    while len(waiting) > 0:
        # f is an i-partial isometry
        f = waiting.pop()
        i = len(f)
        if i == n:
            # f is a full isometry
            if not automorphisms:
                return f
            g = ambient(matrix(f))
            if g not in G:
                G = B.orthogonal_group(tuple(ambient(s.matrix()) for s in G.gens())+(g,))
                waiting = orbits(G, waiting)
            continue
        # extend f to an i+1 - partial isometry in all possible ways
        a = A.smith_form_gens()[i]
        card = ZZ.prod(A.smith_form_gen(k).order() for k in range(i+1))
        for b in b_cand[i]:
            if all(b.b(f[k])==a.b(A.smith_form_gens()[k]) for k in range(i)):
                fnew = f + [b]
                # check that the elements of fnew are independent
                if B.submodule(fnew).cardinality() == card:
                    waiting.append(fnew)
    if not automorphisms:
        raise ValueError("torsion quadratic modules are not isometric")
    gens = G.gap().SmallGeneratingSet()
    return [G(g).matrix() for g in gens]
