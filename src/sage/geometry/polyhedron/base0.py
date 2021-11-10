r"""
Base class for polyhedra, part 0

Initialization and access to Vrepresentation and Hrepresentation.
"""

# ****************************************************************************
#       Copyright (C) 2008-2012 Marshall Hampton <hamptonio@gmail.com>
#       Copyright (C) 2011-2015 Volker Braun <vbraun.name@gmail.com>
#       Copyright (C) 2012-2018 Frederic Chapoton
#       Copyright (C) 2013      Andrey Novoseltsev
#       Copyright (C) 2014-2017 Moritz Firsching
#       Copyright (C) 2014-2019 Thierry Monteil
#       Copyright (C) 2015      Nathann Cohen
#       Copyright (C) 2015-2017 Jeroen Demeyer
#       Copyright (C) 2015-2017 Vincent Delecroix
#       Copyright (C) 2015-2018 Dima Pasechnik
#       Copyright (C) 2015-2020 Jean-Philippe Labbe <labbe at math.huji.ac.il>
#       Copyright (C) 2015-2021 Matthias Koeppe
#       Copyright (C) 2016-2019 Daniel Krenn
#       Copyright (C) 2017      Marcelo Forets
#       Copyright (C) 2017-2018 Mark Bell
#       Copyright (C) 2019      Julian Ritter
#       Copyright (C) 2019-2020 Laith Rastanawi
#       Copyright (C) 2019-2020 Sophia Elia
#       Copyright (C) 2019-2021 Jonathan Kliem <jonathan.kliem@fu-berlin.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ****************************************************************************

from sage.misc.cachefunc import cached_method
from sage.structure.element import Element
import sage.geometry.abc

class Polyhedron_base0(Element, sage.geometry.abc.Polyhedron):
    """
    Initialization and basic access for polyhedra.

    See :class:`sage.geometry.polyhedron.base.Polyhedron_base`.

    TESTS::

        sage: from sage.geometry.polyhedron.base0 import Polyhedron_base0
        sage: P = Polyhedron(rays=[[1, 0, 0]], lines=[[0, 1, 0]])
        sage: Polyhedron_base0.Vrepresentation(P)
        (A line in the direction (0, 1, 0),
        A vertex at (0, 0, 0),
        A ray in the direction (1, 0, 0))
        sage: Polyhedron_base0.vertices.f(P)
        (A vertex at (0, 0, 0),)
        sage: Polyhedron_base0.rays.f(P)
        (A ray in the direction (1, 0, 0),)
        sage: Polyhedron_base0.lines.f(P)
        (A line in the direction (0, 1, 0),)
        sage: Polyhedron_base0.Hrepresentation(P)
        (An equation (0, 0, 1) x + 0 == 0, An inequality (1, 0, 0) x + 0 >= 0)
        sage: Polyhedron_base0.inequalities.f(P)
        (An inequality (1, 0, 0) x + 0 >= 0,)
        sage: Polyhedron_base0.equations.f(P)
        (An equation (0, 0, 1) x + 0 == 0,)
        sage: Polyhedron_base0.base_ring(P)
        Integer Ring
        sage: Polyhedron_base0.backend(P)
        'ppl'
        sage: Polyhedron_base0.change_ring(P, ZZ, backend='field').backend()
        'field'
        sage: Polyhedron_base0.base_extend(P, QQ)
        A 2-dimensional polyhedron in QQ^3 defined as the convex hull of 1 vertex, 1 ray, 1 line
    """
    def __init__(self, parent, Vrep, Hrep, Vrep_minimal=None, Hrep_minimal=None, pref_rep=None, mutable=False, **kwds):
        """
        Initializes the polyhedron.

        See :class:`sage.geometry.polyhedron.base.Polyhedron_base` for a description of the input
        data.

        TESTS::

            sage: p = Polyhedron()    # indirect doctests

            sage: from sage.geometry.polyhedron.backend_field import Polyhedron_field
            sage: from sage.geometry.polyhedron.parent import Polyhedra_field
            sage: parent = Polyhedra_field(AA, 1, 'field')                             # optional - sage.rings.number_field
            sage: Vrep = [[[0], [1/2], [1]], [], []]
            sage: Hrep = [[[0, 1], [1, -1]], []]
            sage: p = Polyhedron_field(parent, Vrep, Hrep,                             # optional - sage.rings.number_field
            ....:                      Vrep_minimal=False, Hrep_minimal=True)
            Traceback (most recent call last):
            ...
            ValueError: if both Vrep and Hrep are provided, they must be minimal...

        Illustration of ``pref_rep``.
        Note that ``ppl`` doesn't support precomputed data::

            sage: from sage.geometry.polyhedron.backend_ppl import Polyhedron_QQ_ppl
            sage: from sage.geometry.polyhedron.parent import Polyhedra_QQ_ppl
            sage: parent = Polyhedra_QQ_ppl(QQ, 1, 'ppl')
            sage: p = Polyhedron_QQ_ppl(parent, Vrep, 'nonsense',
            ....:                       Vrep_minimal=True, Hrep_minimal=True, pref_rep='Vrep')
            sage: p = Polyhedron_QQ_ppl(parent, 'nonsense', Hrep,
            ....:                       Vrep_minimal=True, Hrep_minimal=True, pref_rep='Hrep')
            sage: p = Polyhedron_QQ_ppl(parent, 'nonsense', Hrep,
            ....:                       Vrep_minimal=True, Hrep_minimal=True, pref_rep='Vrepresentation')
            Traceback (most recent call last):
            ...
            ValueError: ``pref_rep`` must be one of ``(None, 'Vrep', 'Hrep')``

        If the backend supports precomputed data, ``pref_rep`` is ignored::

            sage: p = Polyhedron_field(parent, Vrep, 'nonsense',
            ....:                      Vrep_minimal=True, Hrep_minimal=True, pref_rep='Vrep')
            Traceback (most recent call last):
            ...
            TypeError: ..._init_Hrepresentation() takes 3 positional arguments but 9 were given

        The empty polyhedron is detected when the Vrepresentation is given with generator;
        see :trac:`29899`::

            sage: from sage.geometry.polyhedron.backend_cdd import Polyhedron_QQ_cdd
            sage: from sage.geometry.polyhedron.parent import Polyhedra_QQ_cdd
            sage: parent = Polyhedra_QQ_cdd(QQ, 0, 'cdd')
            sage: p = Polyhedron_QQ_cdd(parent, [iter([]), iter([]), iter([])], None)
        """
        Element.__init__(self, parent=parent)
        if Vrep is not None and Hrep is not None:
            if not (Vrep_minimal is True and Hrep_minimal is True):
                raise ValueError("if both Vrep and Hrep are provided, they must be minimal"
                                 " and Vrep_minimal and Hrep_minimal must both be True")
            if hasattr(self, "_init_from_Vrepresentation_and_Hrepresentation"):
                self._init_from_Vrepresentation_and_Hrepresentation(Vrep, Hrep)
                return
            else:
                if pref_rep is None:
                    # Initialize from Hrepresentation if this seems simpler.
                    Vrep = [tuple(Vrep[0]), tuple(Vrep[1]), Vrep[2]]
                    Hrep = [tuple(Hrep[0]), Hrep[1]]
                    if len(Hrep[0]) < len(Vrep[0]) + len(Vrep[1]):
                        pref_rep = 'Hrep'
                    else:
                        pref_rep = 'Vrep'
                if pref_rep == 'Vrep':
                    Hrep = None
                elif pref_rep == 'Hrep':
                    Vrep = None
                else:
                    raise ValueError("``pref_rep`` must be one of ``(None, 'Vrep', 'Hrep')``")
        if Vrep is not None:
            vertices, rays, lines = Vrep

            # We build tuples out of generators now to detect the empty polyhedron.

            # The damage is limited:
            # The backend will have to obtain all elements from the generator anyway.
            # The generators are mainly for saving time with initializing from
            # Vrepresentation and Hrepresentation.
            # If we dispose of one of them (see above), it is wasteful to have generated it.

            # E.g. the dilate will be set up with new Vrepresentation and Hrepresentation
            # regardless of the backend along with the argument ``pref_rep``.
            # As we only use generators, there is no penalty to this approach
            # (and the method ``dilation`` does not have to distinguish by backend).

            if not isinstance(vertices, (tuple, list)):
                vertices = tuple(vertices)
            if not isinstance(rays, (tuple, list)):
                rays = tuple(rays)
            if not isinstance(lines, (tuple, list)):
                lines = tuple(lines)

            if vertices or rays or lines:
                self._init_from_Vrepresentation(vertices, rays, lines, **kwds)
            else:
                self._init_empty_polyhedron()
        elif Hrep is not None:
            ieqs, eqns = Hrep
            self._init_from_Hrepresentation(ieqs, eqns, **kwds)
        else:
            self._init_empty_polyhedron()

    def _init_from_Vrepresentation(self, vertices, rays, lines, **kwds):
        """
        Construct polyhedron from V-representation data.

        INPUT:

        - ``vertices`` -- list of point. Each point can be specified
           as any iterable container of
           :meth:`~sage.geometry.polyhedron.base.base_ring` elements.

        - ``rays`` -- list of rays. Each ray can be specified as any
          iterable container of
          :meth:`~sage.geometry.polyhedron.base.base_ring` elements.

        - ``lines`` -- list of lines. Each line can be specified as
          any iterable container of
          :meth:`~sage.geometry.polyhedron.base.base_ring` elements.

        EXAMPLES::

            sage: p = Polyhedron()
            sage: from sage.geometry.polyhedron.base import Polyhedron_base
            sage: Polyhedron_base._init_from_Vrepresentation(p, [], [], [])
            Traceback (most recent call last):
            ...
            NotImplementedError: a derived class must implement this method
        """
        raise NotImplementedError('a derived class must implement this method')

    def _init_from_Hrepresentation(self, ieqs, eqns, **kwds):
        """
        Construct polyhedron from H-representation data.

        INPUT:

        - ``ieqs`` -- list of inequalities. Each line can be specified
          as any iterable container of
          :meth:`~sage.geometry.polyhedron.base.base_ring` elements.

        - ``eqns`` -- list of equalities. Each line can be specified
          as any iterable container of
          :meth:`~sage.geometry.polyhedron.base.base_ring` elements.

        EXAMPLES::

            sage: p = Polyhedron()
            sage: from sage.geometry.polyhedron.base import Polyhedron_base
            sage: Polyhedron_base._init_from_Hrepresentation(p, [], [])
            Traceback (most recent call last):
            ...
            NotImplementedError: a derived class must implement this method
        """
        raise NotImplementedError('a derived class must implement this method')

    def _init_empty_polyhedron(self):
        """
        Initializes an empty polyhedron.

        TESTS::

            sage: empty = Polyhedron(); empty
            The empty polyhedron in ZZ^0
            sage: empty.Vrepresentation()
            ()
            sage: empty.Hrepresentation()
            (An equation -1 == 0,)
            sage: Polyhedron(vertices = [])
            The empty polyhedron in ZZ^0
            sage: Polyhedron(vertices = [])._init_empty_polyhedron()
            sage: from sage.geometry.polyhedron.parent import Polyhedra
            sage: Polyhedra(QQ,7)()
            A 0-dimensional polyhedron in QQ^7 defined as the convex hull of 1 vertex
        """
        self._Vrepresentation = []
        self._Hrepresentation = []
        self.parent()._make_Equation(self, [-1] + [0] * self.ambient_dim())
        self._Vrepresentation = tuple(self._Vrepresentation)
        self._Hrepresentation = tuple(self._Hrepresentation)

    def base_extend(self, base_ring, backend=None):
        """
        Return a new polyhedron over a larger base ring.

        This method can also be used to change the backend.

        INPUT:

        - ``base_ring`` -- the new base ring

        - ``backend`` -- the new backend, see
          :func:`~sage.geometry.polyhedron.constructor.Polyhedron`.
          If ``None`` (the default), attempt to keep the same backend.
          Otherwise, use the same defaulting behavior
          as described there.

        OUTPUT:

        The same polyhedron, but over a larger base ring and possibly with a changed backend.

        EXAMPLES::

            sage: P = Polyhedron(vertices=[(1,0), (0,1)], rays=[(1,1)], base_ring=ZZ);  P
            A 2-dimensional polyhedron in ZZ^2 defined as the convex hull of 2 vertices and 1 ray
            sage: P.base_extend(QQ)
            A 2-dimensional polyhedron in QQ^2 defined as the convex hull of 2 vertices and 1 ray
            sage: P.base_extend(QQ) == P
            True

        TESTS:

        Test that :trac:`22575` is fixed::

            sage: Q = P.base_extend(ZZ, backend='field')
            sage: Q.backend()
            'field'

        """
        new_parent = self.parent().base_extend(base_ring, backend)
        return new_parent(self, copy=True)

    def change_ring(self, base_ring, backend=None):
        """
        Return the polyhedron obtained by coercing the entries of the
        vertices/lines/rays of this polyhedron into the given ring.

        This method can also be used to change the backend.

        INPUT:

        - ``base_ring`` -- the new base ring

        - ``backend`` -- the new backend or ``None`` (default), see
          :func:`~sage.geometry.polyhedron.constructor.Polyhedron`.
          If ``None`` (the default), attempt to keep the same backend.
          Otherwise, use the same defaulting behavior
          as described there.

        EXAMPLES::

            sage: P = Polyhedron(vertices=[(1,0), (0,1)], rays=[(1,1)], base_ring=QQ); P
            A 2-dimensional polyhedron in QQ^2 defined as the convex hull of 2 vertices and 1 ray
            sage: P.change_ring(ZZ)
            A 2-dimensional polyhedron in ZZ^2 defined as the convex hull of 2 vertices and 1 ray
            sage: P.change_ring(ZZ) == P
            True

            sage: P = Polyhedron(vertices=[(-1.3,0), (0,2.3)], base_ring=RDF); P.vertices()
            (A vertex at (-1.3, 0.0), A vertex at (0.0, 2.3))
            sage: P.change_ring(QQ).vertices()
            (A vertex at (-13/10, 0), A vertex at (0, 23/10))
            sage: P == P.change_ring(QQ)
            True
            sage: P.change_ring(ZZ)
            Traceback (most recent call last):
            ...
            TypeError: cannot change the base ring to the Integer Ring

            sage: P = polytopes.regular_polygon(3); P                           # optional - sage.rings.number_field
            A 2-dimensional polyhedron in AA^2 defined as the convex hull of 3 vertices
            sage: P.vertices()                                                  # optional - sage.rings.number_field
            (A vertex at (0.?e-16, 1.000000000000000?),
             A vertex at (0.866025403784439?, -0.500000000000000?),
             A vertex at (-0.866025403784439?, -0.500000000000000?))
            sage: P.change_ring(QQ)                                             # optional - sage.rings.number_field
            Traceback (most recent call last):
            ...
            TypeError: cannot change the base ring to the Rational Field

        .. WARNING::

            The base ring ``RDF`` should be used with care. As it is
            not an exact ring, certain computations may break or
            silently produce wrong results, for example changing the
            base ring from an exact ring into ``RDF`` may cause a
            loss of data::

                sage: P = Polyhedron([[2/3,0],[6666666666666667/10^16,0]], base_ring=AA); P   # optional - sage.rings.number_field
                A 1-dimensional polyhedron in AA^2 defined as the convex hull of 2 vertices
                sage: Q = P.change_ring(RDF); Q                                 # optional - sage.rings.number_field
                A 0-dimensional polyhedron in RDF^2 defined as the convex hull of 1 vertex
                sage: P.n_vertices() == Q.n_vertices()                          # optional - sage.rings.number_field
                False
        """
        from sage.categories.rings import Rings

        if base_ring not in Rings():
            raise ValueError("invalid base ring")

        try:
            vertices = [[base_ring(x) for x in vertex] for vertex in self.vertices_list()]
            rays = [[base_ring(x) for x in ray] for ray in self.rays_list()]
            lines = [[base_ring(x) for x in line] for line in self.lines_list()]

        except (TypeError, ValueError):
            raise TypeError("cannot change the base ring to the {0}".format(base_ring))

        new_parent = self.parent().change_ring(base_ring, backend)
        return new_parent([vertices, rays, lines], None)

    def is_mutable(self):
        r"""
        Return True if the polyhedron is mutable, i.e. it can be modified in place.

        EXAMPLES::

            sage: p = polytopes.cube(backend='field')
            sage: p.is_mutable()
            False
        """
        return False

    def is_immutable(self):
        r"""
        Return True if the polyhedron is immutable, i.e. it cannot be modified in place.

        EXAMPLES::

            sage: p = polytopes.cube(backend='field')
            sage: p.is_immutable()
            True
        """
        return True

    @cached_method
    def n_equations(self):
        """
        Return the number of equations. The representation will
        always be minimal, so the number of equations is the
        codimension of the polyhedron in the ambient space.

        EXAMPLES::

            sage: p = Polyhedron(vertices = [[1,0,0],[0,1,0],[0,0,1]])
            sage: p.n_equations()
            1
        """
        return len(self.equations())

    @cached_method
    def n_inequalities(self):
        """
        Return the number of inequalities. The representation will
        always be minimal, so the number of inequalities is the
        number of facets of the polyhedron in the ambient space.

        EXAMPLES::

            sage: p = Polyhedron(vertices = [[1,0,0],[0,1,0],[0,0,1]])
            sage: p.n_inequalities()
            3

            sage: p = Polyhedron(vertices = [[t,t^2,t^3] for t in range(6)])
            sage: p.n_facets()
            8
        """
        return len(self.inequalities())

    n_facets = n_inequalities

    @cached_method
    def n_vertices(self):
        """
        Return the number of vertices. The representation will
        always be minimal.

        .. WARNING::

            If the polyhedron has lines, return the number of vertices in
            the ``Vrepresentation``. As the represented polyhedron has
            no 0-dimensional faces (i.e. vertices), ``n_vertices`` corresponds
            to the number of `k`-faces, where `k` is the number of lines::

                sage: P = Polyhedron(rays=[[1,0,0]],lines=[[0,1,0]])
                sage: P.n_vertices()
                1
                sage: P.faces(0)
                ()
                sage: P.f_vector()
                (1, 0, 1, 1)

                sage: P = Polyhedron(rays=[[1,0,0]],lines=[[0,1,0],[0,1,1]])
                sage: P.n_vertices()
                1
                sage: P.f_vector()
                (1, 0, 0, 1, 1)

        EXAMPLES::

            sage: p = Polyhedron(vertices = [[1,0],[0,1],[1,1]], rays=[[1,1]])
            sage: p.n_vertices()
            2
        """
        return len(self.vertices())

    @cached_method
    def n_rays(self):
        """
        Return the number of rays. The representation will
        always be minimal.

        EXAMPLES::

            sage: p = Polyhedron(vertices = [[1,0],[0,1]], rays=[[1,1]])
            sage: p.n_rays()
            1
        """
        return len(self.rays())

    @cached_method
    def n_lines(self):
        """
        Return the number of lines. The representation will
        always be minimal.

        EXAMPLES::

            sage: p = Polyhedron(vertices = [[0,0]], rays=[[0,1],[0,-1]])
            sage: p.n_lines()
            1
        """
        return len(self.lines())

    def Hrepresentation(self, index=None):
        """
        Return the objects of the H-representation. Each entry is
        either an inequality or a equation.

        INPUT:

        - ``index`` -- either an integer or ``None``

        OUTPUT:

        The optional argument is an index running from ``0`` to
        ``self.n_Hrepresentation()-1``. If present, the
        H-representation object at the given index will be
        returned. Without an argument, returns the list of all
        H-representation objects.

        EXAMPLES::

            sage: p = polytopes.hypercube(3, backend='field')
            sage: p.Hrepresentation(0)
            An inequality (-1, 0, 0) x + 1 >= 0
            sage: p.Hrepresentation(0) == p.Hrepresentation()[0]
            True
        """
        if index is None:
            return self._Hrepresentation
        else:
            return self._Hrepresentation[index]

    def Hrepresentation_str(self, separator='\n', latex=False, style='>=', align=None, **kwds):
        r"""
        Return a human-readable string representation of the Hrepresentation of this
        polyhedron.

        INPUT:

        - ``separator`` -- a string. Default is ``"\n"``.

        - ``latex`` -- a boolean. Default is ``False``.

        - ``style`` -- either ``"positive"`` (making all coefficients positive)
                       or ``"<="``, or ``">="``. Default is ``">="``.

        - ``align`` -- a boolean or ``None''. Default is ``None`` in which case
                       ``align`` is ``True`` if ``separator`` is the newline character.
                       If set, then the lines of the output string are aligned
                       by the comparison symbol by padding blanks.

        Keyword parameters of
        :meth:`~sage.geometry.polyhedron.representation.Hrepresentation.repr_pretty`
        are passed on:

        - ``prefix`` -- a string

        - ``indices`` -- a tuple or other iterable

        OUTPUT:

        A string.

        EXAMPLES::

            sage: P = polytopes.permutahedron(3)
            sage: print(P.Hrepresentation_str())
            x0 + x1 + x2 ==  6
                 x0 + x1 >=  3
                -x0 - x1 >= -5
                      x1 >=  1
                     -x0 >= -3
                      x0 >=  1
                     -x1 >= -3

            sage: print(P.Hrepresentation_str(style='<='))
            -x0 - x1 - x2 == -6
                 -x0 - x1 <= -3
                  x0 + x1 <=  5
                      -x1 <= -1
                       x0 <=  3
                      -x0 <= -1
                       x1 <=  3

            sage: print(P.Hrepresentation_str(style='positive'))
            x0 + x1 + x2 == 6
                 x0 + x1 >= 3
                       5 >= x0 + x1
                      x1 >= 1
                       3 >= x0
                      x0 >= 1
                       3 >= x1

            sage: print(P.Hrepresentation_str(latex=True))
            \begin{array}{rcl}
            x_{0} + x_{1} + x_{2} & =    &  6 \\
                    x_{0} + x_{1} & \geq &  3 \\
                   -x_{0} - x_{1} & \geq & -5 \\
                            x_{1} & \geq &  1 \\
                           -x_{0} & \geq & -3 \\
                            x_{0} & \geq &  1 \\
                           -x_{1} & \geq & -3
            \end{array}

            sage: print(P.Hrepresentation_str(align=False))
            x0 + x1 + x2 == 6
            x0 + x1 >= 3
            -x0 - x1 >= -5
            x1 >= 1
            -x0 >= -3
            x0 >= 1
            -x1 >= -3

            sage: c = polytopes.cube()
            sage: c.Hrepresentation_str(separator=', ', style='positive')
            '1 >= x0, 1 >= x1, 1 >= x2, 1 + x0 >= 0, 1 + x2 >= 0, 1 + x1 >= 0'
        """
        pretty_hs = [h.repr_pretty(split=True, latex=latex, style=style, **kwds) for h in self.Hrepresentation()]
        shift = any(pretty_h[2].startswith('-') for pretty_h in pretty_hs)

        if align is None:
            align = separator == "\n"
        if align:
            lengths = [(len(s[0]), len(s[1]), len(s[2])) for s in pretty_hs]
            from operator import itemgetter
            length_left = max(lengths, key=itemgetter(0))[0]
            length_middle = max(lengths, key=itemgetter(1))[1]
            length_right = max(lengths, key=itemgetter(2))[2]
            if shift:
                length_right += 1
            if latex:
                h_line = "{:>" + "{}".format(length_left) + "} & {:" + \
                         "{}".format(length_middle) + "} & {:" + \
                         "{}".format(length_right) + "}\\\\"
            else:
                h_line = "{:>" + "{}".format(length_left) \
                         + "} {:" + "{}".format(length_middle) \
                         + "} {:" + "{}".format(length_right) + "}"
        elif latex:
            h_line = "{} & {} & {}\\\\"
        else:
            h_line = "{} {} {}"

        def pad_non_minus(s):
            if align and shift and not s.startswith('-'):
                return ' ' + s
            else:
                return s
        h_list = [h_line.format(pretty_h[0], pretty_h[1], pad_non_minus(pretty_h[2]))
                  for pretty_h in pretty_hs]
        pretty_print = separator.join(h_list)

        if not latex:
            return pretty_print
        else:
            # below we remove the 2 unnecessary backslashes at the end of pretty_print
            return "\\begin{array}{rcl}\n" + pretty_print[:-2] + "\n\\end{array}"

    def Hrep_generator(self):
        """
        Return an iterator over the objects of the H-representation
        (inequalities or equations).

        EXAMPLES::

            sage: p = polytopes.hypercube(3)
            sage: next(p.Hrep_generator())
            An inequality (-1, 0, 0) x + 1 >= 0
        """
        for H in self.Hrepresentation():
            yield H

    @cached_method
    def n_Hrepresentation(self):
        """
        Return the number of objects that make up the
        H-representation of the polyhedron.

        OUTPUT:

        Integer.

        EXAMPLES::

            sage: p = polytopes.cross_polytope(4)
            sage: p.n_Hrepresentation()
            16
            sage: p.n_Hrepresentation() == p.n_inequalities() + p.n_equations()
            True
        """
        return len(self.Hrepresentation())

    def Vrepresentation(self, index=None):
        """
        Return the objects of the V-representation. Each entry is
        either a vertex, a ray, or a line.

        See :mod:`sage.geometry.polyhedron.constructor` for a
        definition of vertex/ray/line.

        INPUT:

        - ``index`` -- either an integer or ``None``

        OUTPUT:

        The optional argument is an index running from ``0`` to
        ``self.n_Vrepresentation()-1``. If present, the
        V-representation object at the given index will be
        returned. Without an argument, returns the list of all
        V-representation objects.

        EXAMPLES::

            sage: p = polytopes.simplex(4, project=True)
            sage: p.Vrepresentation(0)
            A vertex at (0.7071067812, 0.4082482905, 0.2886751346, 0.2236067977)
            sage: p.Vrepresentation(0) == p.Vrepresentation() [0]
            True
        """
        if index is None:
            return self._Vrepresentation
        else:
            return self._Vrepresentation[index]

    @cached_method
    def n_Vrepresentation(self):
        """
        Return the number of objects that make up the
        V-representation of the polyhedron.

        OUTPUT:

        Integer.

        EXAMPLES::

            sage: p = polytopes.simplex(4)
            sage: p.n_Vrepresentation()
            5
            sage: p.n_Vrepresentation() == p.n_vertices() + p.n_rays() + p.n_lines()
            True
        """
        return len(self.Vrepresentation())

    def Vrep_generator(self):
        """
        Return an iterator over the objects of the V-representation
        (vertices, rays, and lines).

        EXAMPLES::

            sage: p = polytopes.cyclic_polytope(3,4)
            sage: vg = p.Vrep_generator()
            sage: next(vg)
            A vertex at (0, 0, 0)
            sage: next(vg)
            A vertex at (1, 1, 1)
        """
        for V in self.Vrepresentation():
            yield V

    def inequality_generator(self):
        """
        Return  a generator for the defining inequalities of the
        polyhedron.

        OUTPUT:

        A generator of the inequality Hrepresentation objects.

        EXAMPLES::

            sage: triangle = Polyhedron(vertices=[[1,0],[0,1],[1,1]])
            sage: for v in triangle.inequality_generator(): print(v)
            An inequality (1, 1) x - 1 >= 0
            An inequality (0, -1) x + 1 >= 0
            An inequality (-1, 0) x + 1 >= 0
            sage: [ v for v in triangle.inequality_generator() ]
            [An inequality (1, 1) x - 1 >= 0,
             An inequality (0, -1) x + 1 >= 0,
             An inequality (-1, 0) x + 1 >= 0]
            sage: [ [v.A(), v.b()] for v in triangle.inequality_generator() ]
            [[(1, 1), -1], [(0, -1), 1], [(-1, 0), 1]]
        """
        for H in self.Hrepresentation():
            if H.is_inequality():
                yield H

    @cached_method
    def inequalities(self):
        """
        Return all inequalities.

        OUTPUT:

        A tuple of inequalities.

        EXAMPLES::

            sage: p = Polyhedron(vertices = [[0,0,0],[0,0,1],[0,1,0],[1,0,0],[2,2,2]])
            sage: p.inequalities()[0:3]
            (An inequality (1, 0, 0) x + 0 >= 0,
             An inequality (0, 1, 0) x + 0 >= 0,
             An inequality (0, 0, 1) x + 0 >= 0)

            sage: p3 = Polyhedron(vertices=Permutations([1, 2, 3, 4]))          # optional - sage.combinat
            sage: ieqs = p3.inequalities()                                      # optional - sage.combinat
            sage: ieqs[0]                                                       # optional - sage.combinat
            An inequality (0, 1, 1, 1) x - 6 >= 0
            sage: list(_)                                                       # optional - sage.combinat
            [-6, 0, 1, 1, 1]
        """
        return tuple(self.inequality_generator())

    def inequalities_list(self):
        """
        Return a list of inequalities as coefficient lists.

        .. NOTE::

            It is recommended to use :meth:`inequalities` or
            :meth:`inequality_generator` instead to iterate over the
            list of :class:`Inequality` objects.

        EXAMPLES::

            sage: p = Polyhedron(vertices = [[0,0,0],[0,0,1],[0,1,0],[1,0,0],[2,2,2]])
            sage: p.inequalities_list()[0:3]
            [[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

            sage: p3 = Polyhedron(vertices=Permutations([1, 2, 3, 4]))          # optional - sage.combinat
            sage: ieqs = p3.inequalities_list()                                 # optional - sage.combinat
            sage: ieqs[0]                                                       # optional - sage.combinat
            [-6, 0, 1, 1, 1]
            sage: ieqs[-1]                                                      # optional - sage.combinat
            [-3, 0, 1, 0, 1]
            sage: ieqs == [list(x) for x in p3.inequality_generator()]          # optional - sage.combinat
            True
        """
        return [list(x) for x in self.inequality_generator()]

    def equation_generator(self):
        """
        Return a generator for the linear equations satisfied by the
        polyhedron.

        EXAMPLES::

            sage: p = polytopes.regular_polygon(8,base_ring=RDF)
            sage: p3 = Polyhedron(vertices = [x+[0] for x in p.vertices()], base_ring=RDF)
            sage: next(p3.equation_generator())
            An equation (0.0, 0.0, 1.0) x + 0.0 == 0
        """
        for H in self.Hrepresentation():
            if H.is_equation():
                yield H

    @cached_method
    def equations(self):
        """
        Return all linear constraints of the polyhedron.

        OUTPUT:

        A tuple of equations.

        EXAMPLES::

            sage: test_p = Polyhedron(vertices = [[1,2,3,4],[2,1,3,4],[4,3,2,1],[3,4,1,2]])
            sage: test_p.equations()
            (An equation (1, 1, 1, 1) x - 10 == 0,)
        """
        return tuple(self.equation_generator())

    def equations_list(self):
        """
        Return the linear constraints of the polyhedron. As with
        inequalities, each constraint is given as [b -a1 -a2 ... an]
        where for variables x1, x2,..., xn, the polyhedron satisfies
        the equation b = a1*x1 + a2*x2 + ... + an*xn.

        .. NOTE::

            It is recommended to use :meth:`equations` or
            :meth:`equation_generator()` instead to iterate over the
            list of
            :class:`~sage.geometry.polyhedron.representation.Equation`
            objects.

        EXAMPLES::

            sage: test_p = Polyhedron(vertices = [[1,2,3,4],[2,1,3,4],[4,3,2,1],[3,4,1,2]])
            sage: test_p.equations_list()
            [[-10, 1, 1, 1, 1]]
        """
        return [list(eq) for eq in self.equation_generator()]

    def vertices_list(self):
        """
        Return a list of vertices of the polyhedron.

        .. NOTE::

            It is recommended to use :meth:`vertex_generator` instead to
            iterate over the list of :class:`Vertex` objects.

        .. WARNING::

            If the polyhedron has lines, return the vertices
            of the ``Vrepresentation``. However, the represented polyhedron
            has no 0-dimensional faces (i.e. vertices)::

                sage: P = Polyhedron(rays=[[1,0,0]],lines=[[0,1,0]])
                sage: P.vertices_list()
                [[0, 0, 0]]
                sage: P.faces(0)
                ()

        EXAMPLES::

            sage: triangle = Polyhedron(vertices=[[1,0],[0,1],[1,1]])
            sage: triangle.vertices_list()
            [[0, 1], [1, 0], [1, 1]]
            sage: a_simplex = Polyhedron(ieqs = [
            ....:          [0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1]
            ....:      ], eqns = [[1,-1,-1,-1,-1]])
            sage: a_simplex.vertices_list()
            [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
            sage: a_simplex.vertices_list() == [list(v) for v in a_simplex.vertex_generator()]
            True
        """
        return [list(x) for x in self.vertex_generator()]

    def vertex_generator(self):
        """
        Return a generator for the vertices of the polyhedron.

        .. WARNING::

            If the polyhedron has lines, return a generator for the vertices
            of the ``Vrepresentation``. However, the represented polyhedron
            has no 0-dimensional faces (i.e. vertices)::

                sage: P = Polyhedron(rays=[[1,0,0]],lines=[[0,1,0]])
                sage: list(P.vertex_generator())
                [A vertex at (0, 0, 0)]
                sage: P.faces(0)
                ()

        EXAMPLES::

            sage: triangle = Polyhedron(vertices=[[1,0],[0,1],[1,1]])
            sage: for v in triangle.vertex_generator(): print(v)
            A vertex at (0, 1)
            A vertex at (1, 0)
            A vertex at (1, 1)
            sage: v_gen = triangle.vertex_generator()
            sage: next(v_gen)   # the first vertex
            A vertex at (0, 1)
            sage: next(v_gen)   # the second vertex
            A vertex at (1, 0)
            sage: next(v_gen)   # the third vertex
            A vertex at (1, 1)
            sage: try: next(v_gen)   # there are only three vertices
            ....: except StopIteration: print("STOP")
            STOP
            sage: type(v_gen)
            <... 'generator'>
            sage: [ v for v in triangle.vertex_generator() ]
            [A vertex at (0, 1), A vertex at (1, 0), A vertex at (1, 1)]
        """
        for V in self.Vrepresentation():
            if V.is_vertex():
                yield V

    @cached_method
    def vertices(self):
        """
        Return all vertices of the polyhedron.

        OUTPUT:

        A tuple of vertices.

        .. WARNING::

            If the polyhedron has lines, return the vertices
            of the ``Vrepresentation``. However, the represented polyhedron
            has no 0-dimensional faces (i.e. vertices)::

                sage: P = Polyhedron(rays=[[1,0,0]],lines=[[0,1,0]])
                sage: P.vertices()
                (A vertex at (0, 0, 0),)
                sage: P.faces(0)
                ()

        EXAMPLES::

            sage: triangle = Polyhedron(vertices=[[1,0],[0,1],[1,1]])
            sage: triangle.vertices()
            (A vertex at (0, 1), A vertex at (1, 0), A vertex at (1, 1))
            sage: a_simplex = Polyhedron(ieqs = [
            ....:          [0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1]
            ....:      ], eqns = [[1,-1,-1,-1,-1]])
            sage: a_simplex.vertices()
            (A vertex at (1, 0, 0, 0), A vertex at (0, 1, 0, 0),
             A vertex at (0, 0, 1, 0), A vertex at (0, 0, 0, 1))
        """
        return tuple(self.vertex_generator())

    def ray_generator(self):
        """
        Return a generator for the rays of the polyhedron.

        EXAMPLES::

            sage: pi = Polyhedron(ieqs = [[1,1,0],[1,0,1]])
            sage: pir = pi.ray_generator()
            sage: [x.vector() for x in pir]
            [(1, 0), (0, 1)]
        """
        for V in self.Vrepresentation():
            if V.is_ray():
                yield V

    @cached_method
    def rays(self):
        """
        Return a list of rays of the polyhedron.

        OUTPUT:

        A tuple of rays.

        EXAMPLES::

            sage: p = Polyhedron(ieqs = [[0,0,0,1],[0,0,1,0],[1,1,0,0]])
            sage: p.rays()
            (A ray in the direction (1, 0, 0),
             A ray in the direction (0, 1, 0),
             A ray in the direction (0, 0, 1))
        """
        return tuple(self.ray_generator())

    def rays_list(self):
        """
        Return a list of rays as coefficient lists.

        .. NOTE::

            It is recommended to use :meth:`rays` or
            :meth:`ray_generator` instead to iterate over the list of
            :class:`Ray` objects.

        OUTPUT:

        A list of rays as lists of coordinates.

        EXAMPLES::

            sage: p = Polyhedron(ieqs = [[0,0,0,1],[0,0,1,0],[1,1,0,0]])
            sage: p.rays_list()
            [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            sage: p.rays_list() == [list(r) for r in p.ray_generator()]
            True
        """
        return [list(x) for x in self.ray_generator()]

    def line_generator(self):
        """
        Return a generator for the lines of the polyhedron.

        EXAMPLES::

            sage: pr = Polyhedron(rays = [[1,0],[-1,0],[0,1]], vertices = [[-1,-1]])
            sage: next(pr.line_generator()).vector()
            (1, 0)
        """
        for V in self.Vrepresentation():
            if V.is_line():
                yield V

    @cached_method
    def lines(self):
        """
        Return all lines of the polyhedron.

        OUTPUT:

        A tuple of lines.

        EXAMPLES::

            sage: p = Polyhedron(rays = [[1,0],[-1,0],[0,1],[1,1]], vertices = [[-2,-2],[2,3]])
            sage: p.lines()
            (A line in the direction (1, 0),)
        """
        return tuple(self.line_generator())

    def lines_list(self):
        """
        Return a list of lines of the polyhedron.  The line data is given
        as a list of coordinates rather than as a Hrepresentation object.

        .. NOTE::

            It is recommended to use :meth:`line_generator` instead to
            iterate over the list of :class:`Line` objects.

        EXAMPLES::

            sage: p = Polyhedron(rays = [[1,0],[-1,0],[0,1],[1,1]], vertices = [[-2,-2],[2,3]])
            sage: p.lines_list()
            [[1, 0]]
            sage: p.lines_list() == [list(x) for x in p.line_generator()]
            True
        """
        return [list(x) for x in self.line_generator()]

    def base_ring(self):
        """
        Return the base ring.

        OUTPUT:

        The ring over which the polyhedron is defined. Must be a
        sub-ring of the reals to define a polyhedron, in particular
        comparison must be defined. Popular choices are

        * ``ZZ`` (the ring of integers, lattice polytope),

        * ``QQ`` (exact arithmetic using gmp),

        * ``RDF`` (double precision floating-point arithmetic), or

        * ``AA`` (real algebraic field).

        EXAMPLES::

            sage: triangle = Polyhedron(vertices = [[1,0],[0,1],[1,1]])
            sage: triangle.base_ring() == ZZ
            True
        """
        return self.parent().base_ring()

    def backend(self):
        """
        Return the backend used.

        OUTPUT:

        The name of the backend used for computations. It will be one of
        the following backends:

         * ``ppl`` the Parma Polyhedra Library

         * ``cdd`` CDD

         * ``normaliz`` normaliz

         * ``polymake`` polymake

         * ``field`` a generic Sage implementation

        EXAMPLES::

            sage: triangle = Polyhedron(vertices = [[1, 0], [0, 1], [1, 1]])
            sage: triangle.backend()
            'ppl'
            sage: D = polytopes.dodecahedron()  # optional - sage.rings.number_field
            sage: D.backend()                   # optional - sage.rings.number_field
            'field'
            sage: P = Polyhedron([[1.23]])
            sage: P.backend()
            'cdd'
        """
        return self.parent().backend()