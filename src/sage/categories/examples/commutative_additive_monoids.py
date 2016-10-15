"""
Examples of commutative additive monoids
"""
from __future__ import absolute_import
#*****************************************************************************
#  Copyright (C) 2008-2009 Nicolas M. Thiery <nthiery at users.sf.net>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#******************************************************************************

from sage.misc.cachefunc import cached_method
from sage.structure.parent import Parent
from sage.categories.all import CommutativeAdditiveMonoids
from .commutative_additive_semigroups import FreeCommutativeAdditiveSemigroup

class FreeCommutativeAdditiveMonoid(FreeCommutativeAdditiveSemigroup):
    r"""
    An example of a commutative additive monoid: the free commutative monoid

    This class illustrates a minimal implementation of a commutative monoid.

    EXAMPLES::

        sage: S = CommutativeAdditiveMonoids().example(); S
        An example of a commutative monoid: the free commutative monoid generated by ('a', 'b', 'c', 'd')

        sage: S.category()
        Category of commutative additive monoids

    This is the free semigroup generated by::

        sage: S.additive_semigroup_generators()
        Family (a, b, c, d)

    with product rule given by $a \times b = a$ for all $a, b$::

        sage: (a,b,c,d) = S.additive_semigroup_generators()

    We conclude by running systematic tests on this commutative monoid::

        sage: TestSuite(S).run(verbose = True)
        running ._test_additive_associativity() . . . pass
        running ._test_an_element() . . . pass
        running ._test_cardinality() . . . pass
        running ._test_category() . . . pass
        running ._test_elements() . . .
          Running the test suite of self.an_element()
          running ._test_category() . . . pass
          running ._test_eq() . . . pass
          running ._test_nonzero_equal() . . . pass
          running ._test_not_implemented_methods() . . . pass
          running ._test_pickling() . . . pass
          pass
        running ._test_elements_eq_reflexive() . . . pass
        running ._test_elements_eq_symmetric() . . . pass
        running ._test_elements_eq_transitive() . . . pass
        running ._test_elements_neq() . . . pass
        running ._test_eq() . . . pass
        running ._test_not_implemented_methods() . . . pass
        running ._test_pickling() . . . pass
        running ._test_some_elements() . . . pass
        running ._test_zero() . . . pass
    """

    def __init__(self, alphabet=('a','b','c','d')):
        r"""
        The free commutative monoid

        INPUT:

         - ``alphabet`` -- a tuple of strings: the generators of the monoid

        EXAMPLES::

            sage: M = CommutativeAdditiveMonoids().example(alphabet=('a','b','c')); M
            An example of a commutative monoid: the free commutative monoid generated by ('a', 'b', 'c')

        TESTS::

            sage: TestSuite(M).run()

        """
        self.alphabet = alphabet
        Parent.__init__(self, category = CommutativeAdditiveMonoids())

    def _repr_(self):
        r"""
        TESTS::

            sage: M = CommutativeAdditiveMonoids().example(alphabet=('a','b','c'))
            sage: M._repr_()
            "An example of a commutative monoid: the free commutative monoid generated by ('a', 'b', 'c')"

        """
        return "An example of a commutative monoid: the free commutative monoid generated by %s"%(self.alphabet,)

    @cached_method
    def zero(self):
        r"""
        Returns the zero of this additive monoid, as per :meth:`CommutativeAdditiveMonoids.ParentMethods.zero`.

        EXAMPLES::

            sage: M = CommutativeAdditiveMonoids().example(); M
            An example of a commutative monoid: the free commutative monoid generated by ('a', 'b', 'c', 'd')
            sage: M.zero()
            0
        """
        return self(())

    class Element(FreeCommutativeAdditiveSemigroup.Element):
        def __bool__(self):
            """
            Check if ``self`` is not the zero of the monoid

            EXAMPLES::

                sage: M = CommutativeAdditiveMonoids().example()
                sage: bool(M.zero())
                False
                sage: [bool(m) for m in M.additive_semigroup_generators()]
                [True, True, True, True]
            """
            return any(x for x in self.value.values())

        __nonzero__ = __bool__

Example = FreeCommutativeAdditiveMonoid
