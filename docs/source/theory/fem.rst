.. _sec_theory_fem:

FEM formulation
===============

The governing equations :eq:`u_x` to :eq:`t_x` for the |eb| beam are conveniently solved using a FE formulation which is well suited for computational analyses. The FE discretisation can be constructed from the governing equations using the *Galerkin weighted residual method*. This section summarises the basic idea of the Galerkin method as well as the FE formulation implemented in the structure tool |name|. More detailed theoretical background on the FEM_ can be found in [CMPW02]_, [Prze85]_, [Bath14]_, [SmGM14]_.

Galerkin weighted residual method
---------------------------------

In the following, the *Galerkin weighted residual method* (henceforth simply called Galerkin method) is outlined. This summary is partly based on [CMPW02]_, [Prze85]_ where further details are given. The Galerkin method "converts" the governing differential equations into a discretised problem, eventually formulating a system of linear equations from which an approximate solution can be obtained. In general terms, a physical problem may be stated in the form

.. math::
    :label: eq_galerkin_problem_general

    D u - f = 0

where :math:`D` is a differential operator, :math:`u = u(x)` are dependent variables (e.g. displacements of a material point), :math:`x` are independent variables (e.g. coordinates of a material point) and :math:`f` is a function of :math:`x` (:math:`f` may be constant or zero). Note that the governing equations for the |eb| beam are stated in this form.

The next step in the Galerkin method is to choose an approximating solution :math:`\widetilde{u}` for :math:`u` which does not (have to) satisfy eq. :eq:`eq_galerkin_problem_general` in *every* point. Due to the approximation a residual :math:`R = R(x)` may remain. Equation :eq:`eq_galerkin_problem_general` becomes

.. math::
    :label: eq_galerkin_problem_general_residual

    D \widetilde{u} - f = R

Typically, one chooses a polynomial for the approximating function like :math:`\widetilde{u}(x) = a_0 + a_1 \cdot x + a_2 \cdot x^2 \dots`, where the coefficients :math:`a_\text{i}` are chosen so that :math:`R` is small (in some sense). Next, one formulates a so-called *weak form*. The governing equations are no longer required to be satisfied exactly in every point but rather over the integral of a domain :math:`V`, i.e. in an average sense.

.. math::
    :label: eq_galerkin_residual_equation

    \displaystyle\int_V W_\text{i} \cdot R \,\text{d}{V} = 0 \qquad \text{for} \qquad i = 1, 2, \dots, n

The :math:`W_\text{i} = W_\text{i} (x)` are so-called weight functions. In the FEM_ formulation, the :math:`a_\text{i}` are nodal deformations which are usually the primary unknowns as shown in the following example.

Example
~~~~~~~

To illustrate the Galerkin method, the procedure will be shown for a uniform bar in axial loading (:numref:`fig_bar_element` a). The equation of motion is

.. math::
    :label: eq_gov_eq_bar_element

    \frac{\partial{}}{\partial{x}} \left( E \cdot A \cdot \frac{\partial{u_x}}{\partial{x}} \right) + q_x - \varrho \cdot A \frac{\partial{}^2 u_x}{\partial{t}^2} = 0

This equation has already been stated in eq. :eq:`u_x` as part of the beam equations, though without the inertia term which introduces a time dependency (:math:`t`). Equation :eq:`eq_gov_eq_bar_element` is also referred to as the *strong form* of the governing equations, since a solution :math:`u_x(x,t)` has to satisfy the equation in every point :math:`x` and for every point in time :math:`t`. At any arbitrary :math:`x`, the axial force in the bar is

.. math::
    :label: eq_bar_element_Fx

    F_x = A \cdot \sigma_x = E \cdot A \cdot \epsilon_x = E \cdot A \cdot \frac{\partial{}u_x}{\partial{x}}

where :math:`\sigma_x` and :math:`\epsilon_x` are the axial stress and strain, respectively.

.. _fig_bar_element:
.. figure:: ../_static/images/theory/bar_element.svg
   :width: 800 px
   :alt: Bar element
   :align: center

   **(a)** 1D bar element under distributed axial loading :math:`q_x = q_x(x)`. **(b)** Two adjacent elements from the discretised bar. After the resulting system of equations is assembled, node *b* is shared (figure adapted from [CMPW02]_).

With a separation of variables an approximating solution for eq. :eq:`eq_gov_eq_bar_element` of a discretised bar (:numref:`fig_bar_element` b) may be formulated in the form

.. math::
    :label: eq_ux_approx

    \widetilde{u}_x(x,t) = \sum_{j=1}^n d_\text{j}(t) \cdot N_\text{j} (x)

where :math:`d_\text{j}` are unknown coefficients (here the nodal displacements), and :math:`N_\text{j}` are referred to as FEM_ *shape functions* which also serve as Galerkin weight functions. The Galerkin residual eq. :eq:`eq_galerkin_residual_equation` becomes

.. math::
    :label: eq_galerkin_residual_for_bar

    \displaystyle\int_0^L N_\text{i} \cdot \left[ \sum_{j=1}^n \left( E \cdot A \cdot d_\text{j} \cdot N_\text{j}^\prime \right)' + q_x - \sum_{j=1}^n \varrho \cdot A \cdot \ddot{d}_\text{j} \cdot N_\text{j}  \right] \text{d}{x} = 0

In this case, the domain :math:`V` is the entire bar structure, i.e. the length of the bar :math:`L`. The indices :math:`i` and :math:`j` range over all shape functions (:math:`i, j = 1, 2, \dots, n`). Integrating by parts, rearranging the order of operations and substituting the force :math:`F_x` from eq. :eq:`eq_bar_element_Fx` yields

.. math::
    :label: eq_galerkin_residual_for_bar_proc2

    \sum_{j=1}^n \underbrace{ E \cdot A \displaystyle\int_0^L N'_\text{i} \cdot N'_\text{j} \,\text{d}{x} }_{K_{\text{i}\text{j}}} \cdot d_\text{j}
    &- \sum_{j=1}^n \underbrace{ \varrho \cdot A \displaystyle\int_0^L N_\text{i} \cdot N_\text{j} \,\text{d}{x} }_{M_{\text{i}\text{j}}} \cdot \ddot{d}_\text{j} \nonumber \\
    &= \displaystyle\int_0^L N_\text{i} \cdot q_x \,\text{d}{x} + \left[ N_\text{i} \sum_{j=1}^n F_{x,\text{j}} \right]_0^L

This equation pretty much resembles the sought-after FEM_ formulation. The highlighted terms :math:`K_{\text{i}\text{j}}` and :math:`M_{\text{i}\text{j}}` are elements of the global stiffness matrix :math:`\mathbf{K}` and mass matrix :math:`\mathbf{M}`, respectively. The summation symbolises the assembly process. The result becomes even clearer when choosing shape functions and performing the integrations. For the sake of simplicity, the bar is divided into a single element (:math:`i, j = 1, 2`). As a result of the integration by parts, the second order derivative from eq. :eq:`eq_gov_eq_bar_element` disappeared. Therefore, the approximating function :math:`\widetilde{u}_x` can be of lower order than required by the original governing eq. :eq:`eq_gov_eq_bar_element`. For a bar it is sufficient to approximate the displacement field using element-wise *linear* functions.

.. math::

    \widetilde{u}_x(x,t) &= \mathbf{N}(x) \cdot \mathbf{d}(t) \\
    \quad \text{with} \quad
    \mathbf{N} &= \left( N_1, N_2 \right) =
    \left( 1 - \frac{x}{l_e}, \frac{x}{l_e} \right) \\
    \quad \text{and} \quad
    \mathbf{d} &=
    \begin{pmatrix}
        u_1(t)\\
        u_2(t)
    \end{pmatrix}

where :math:`x=0` at the left end of the element. The coefficients :math:`u_1` and :math:`u_2` have the same purpose as the :math:`a_\text{i}` mentioned above. Here, they are nodal displacements of the element (notice that :math:`N_\text{i}` is either 0 or 1 at the ends of the element, here :math:`l_e=L`). For a bar made up of a single element, eq. :eq:`eq_galerkin_residual_for_bar_proc2` becomes

.. math::
    :label: eq_bar_galerkin_almost_there

    E \cdot A \cdot \displaystyle\int_0^{L} \mathbf{B}^T \cdot \mathbf{B} \,\text{d}{x} \cdot \mathbf{d}
    &- \varrho \cdot A \cdot \displaystyle\int_0^{L} \mathbf{N}^T \cdot \mathbf{N} \,\text{d}{x} \cdot \ddot{\mathbf{d}}
    = \displaystyle\int_0^{L} \mathbf{N}^T \cdot q_x \,\text{d}{x}
    + \bigl[ \mathbf{N}^T \cdot F_x \bigr]_0^{L} \\
    %%
    %%
    %%
    \text{where} \qquad \mathbf{B} &{:=} \mathbf{N}' \nonumber \\
    %%
    %%
    %%
    \label{eq:bar_galerkin_more_like_fem}
    \underbrace{
    \frac{E \cdot A}{L} \cdot
    \begin{bmatrix}
        1  & -1 \\
        -1 &  1 \\
    \end{bmatrix}
    }_{\mathbf{K}}
    \underbrace{
    \begin{pmatrix}
        u_1 \\
        u_2 \\
    \end{pmatrix}
    }_{\mathbf{d} = \mathbf{U}}
    &+
    \underbrace{
    \frac{-\varrho \cdot A \cdot L}{6} \cdot
    \begin{bmatrix}
        2 & 1 \\
        1 & 2 \\
    \end{bmatrix}
    }_{\mathbf{M}}
    \underbrace{
    \begin{pmatrix}
        \ddot{u}_1 \\
        \ddot{u}_2 \\
    \end{pmatrix}
    }_{\ddot{\mathbf{d}} = \ddot{\mathbf{U}}}
    =
    \underbrace{
    \begin{pmatrix}
        1/2 \\
        1/2
    \end{pmatrix}
    q_x
    +
    \begin{pmatrix}
        F_{x,1} \\
        F_{x,2}
    \end{pmatrix}
    }_{\mathbf{F}}

This is the well known FEM_ formulation, :math:`\mathbf{K} \cdot \mathbf{U} + \mathbf{M} \cdot \ddot{\mathbf{U}} = \mathbf{F}`. The term :math:`\mathbf{K} \cdot \mathbf{U}` represents internal elastic loads, and :math:`\mathbf{M} \cdot \ddot{\mathbf{U}}` represents the inertia loads. The right-hand side represents the external loads :math:`\mathbf{F}`. The second term in :math:`\mathbf{F}` involves the boundary conditions at the left and right end of the bar. The initial governing differential equation is now discretised and transformed into a system of equations.

In general, the discretised formulation is not equal to the exact solution but the FE formulation converges to the exact solution of the mathematical model as the mesh is refined. The rate of convergence is influenced by the choice of the shape functions. A similar procedure as shown for the bar element can be applied to derive the matrices for the *beam* which has additional |dof| for bending and torsion.

The beam element
----------------

Beams are divided into *elements* which form the core of the FE formulation. A beam element consists of two nodes, numbered :math:`i` and :math:`i+1` in a global "bookkeeping" system (:numref:`fig_beam_element`). It is worth to point out that a 3D beam element is not uniquely defined by two points (nodes) in space. As the element contains directional information, namely bending stiffness :math:`E \cdot I_y` and :math:`E \cdot I_z` defined in a local (cross section) coordinate system, such a local system has to be defined as part of the user input. The orientation of the local coordinate system may be provided as an "upwards" direction (:math:`z`-direction), or using angles with respect to the global coordinate system.

.. _fig_beam_element:
.. figure:: ../_static/images/theory/beam_element_dof.svg
   :width: 500 px
   :alt: Beam element
   :align: center

   Beam element with translational and rotational |dof_long|. The global coordinate system is indicated in blue and the element-local coordinate system (located in the element centre) in green. In the global structure system (including all elements) the nodes have numbers :math:`i` and :math:`i+\text{i}`. Within an element these nodes are numbered 1 and 2.

Each beam element has six translational and six rotational |dof|. These may be summarised in an *element displacement vector*,

.. math::
    :label: eq_element_displacement_vector

    \mathbf{U}_\text{e,loc} &=
    (\mathbf{U}_1, \boldsymbol{\Theta}_1, \mathbf{U}_2, \boldsymbol{\Theta}_2)^T_\text{loc} \\
    &= \left(
        u_{x,1}, u_{y,1}, u_{z,1},
        \Theta_{x,1}, \Theta_{y,1}, \Theta_{z,1},
        %%
        u_{x,2}, u_{y,2}, u_{z,2},
        \Theta_{x,2}, \Theta_{y,2}, \Theta_{z,2}
    \right)_\text{loc}^T

where the subscript *e* indicates the *element* and *loc* the formulation with respect to the *local* system. The deformation in between two nodes is given by *shape functions* as :math:`\mathbf{U}_{\text{e},\xi} = (u_x, u_y, u_z, \Theta_x, \Theta_y, \Theta_z)_{\text{e},\xi}^T = \mathbf{N} \cdot \mathbf{U}_\text{e, loc}`. The shape function matrix :math:`\mathbf{N}` for the \EulerBernoulli beam is (c.f. [CMPW02]_)

.. math::
    :label: eq_shape_funtion_matrix

    \mathbf{N} =
    \begin{bmatrix}
        N_1 & 0    & 0   & 0   & 0    & 0   & N_2 & 0    & 0   & 0   & 0    & 0 \\
        0   & N_3  & 0   & 0   & 0    & N_5 & 0   & N_4  & 0   & 0   & 0    & N_6 \\
        0   & 0    & N_3 & 0   & -N_5 & 0   & 0   & 0    & N_4 & 0   & -N_6 & 0 \\
        0   & 0    & 0   & M_1 & 0    & 0   & 0   & 0    & 0   & M_2 & 0    & 0 \\
        0   & 0    & M_3 & 0   & M_5  & 0   & 0   & 0    & M_4 & 0   & M_6  & 0 \\
        0   & -M_3 & 0   & 0   & 0    & M_5 & 0   & -M_4 & 0   & 0   & 0    & M_6
    \end{bmatrix}

with the shape functions

.. math::

        N_1 &= 1 - \xi \\[2mm]
        N_2 &= \xi \\[2mm]
        N_3 &= 1 - 3 \cdot \xi^2 +  2 \cdot \xi^3 \\[2mm]
        N_4 &= 3 \cdot \xi^2 - 2 \cdot \xi^3 \\[2mm]
        N_5 &= l_e ( \xi - 2 \cdot \xi^2 + \xi^3) \\[2mm]
        N_6 &= l_e ( -\xi^2 + \xi^3) \\
        M_1 &= 1 - \xi \\
        M_2 &= \xi \\
        M_3 &= \frac{\text{d}{N_3}}{\text{d}{\bar{x}}} = -\frac{6}{l_e} \cdot (\xi - \xi^2) \\
        M_4 &= \frac{\text{d}{N_4}}{\text{d}{\bar{x}}} = \frac{6}{l_e} \cdot (\xi - \xi^2) \\
        M_5 &= \frac{\text{d}{N_5}}{\text{d}{\bar{x}}} = 1 - 4 \cdot \xi + 3 \cdot \xi^2 \\
        M_6 &= \frac{\text{d}{N_6}}{\text{d}{\bar{x}}} = -2 \cdot \xi + 3 \cdot \xi^2

        \text{with} \quad \xi := \frac{\bar{x}}{l_e} \qquad \text{where} \quad \bar{x} := \frac{l_e}{2} + x

The variable :math:`\xi` is a relative element coordinate. At the "left" element node :math:`\xi` is zero and at the "right" node :math:`\xi` is one (see :numref:`fig_beam_element`). The last two rows in the shape function matrix are used to describe :math:`\Theta_y(\xi)` and :math:`\Theta_z(\xi)` which are related through the kinematic relations stated in eq. :eq:`eq_angles_euler_bernoulli`.

The *element stiffness matrix* is (c.f. [CMPW02]_, [Prze85]_)

.. math::
    :label: eq_element_stiffness_matrix

    \mathbf{K}_\text{e,loc} =
    \begin{bmatrix}
        %% line 1
        \frac{E \cdot A}{l_e} & 0 & 0 & 0 & 0 & 0 &
        -\frac{E \cdot A}{l_e} & 0 & 0 & 0 & 0 & 0 \\
        %% line 2
        ~ & \frac{12 E \cdot I_z}{l_e^3} & 0 & 0 & 0 & \frac{6 E \cdot I_z}{l_e^2} &
        0 & -\frac{12 E \cdot I_z}{l_e^3} & 0 & 0 & 0 & \frac{6 E \cdot I_z}{l_e^2} \\
        %% line 3
        ~ & ~ & \frac{12 E \cdot I_y}{l_e^3} & 0 & -\frac{6 E \cdot I_y}{l_e^2} & 0 &
        0 & 0 & -\frac{12 E \cdot I_y}{l_e^3} & 0 & -\frac{6 E \cdot I_y}{l_e^2} & 0 \\
        %% line 4
        ~ & ~ & ~ & \frac{G \cdot J}{l_e} & 0 & 0 &
        0 & 0 & 0 & -\frac{G \cdot J}{l_e} & 0 & 0 \\
        %% line 5
        ~ & ~ & ~ & ~ & \frac{4 E \cdot I_y}{l_e} & 0 &
        0 & 0 & \frac{6 E \cdot I_y}{l_e^2} & 0 & \frac{2 E \cdot I_y}{l_e} & 0 \\
        %% line 6
        ~ & ~ & ~ & ~ & ~ & \frac{4 E \cdot I_z}{l_e} &
        0 & -\frac{6 E \cdot I_z}{l_e^2} & 0 & 0 & 0 & \frac{2 E \cdot I_z}{l_e} \\
        %% line 7
        ~ & ~ & ~ & ~ & ~ & ~ &
        \frac{E \cdot A}{l_e} & 0 & 0 & 0 & 0 & 0 \\
        %% line 8
        ~ & ~ & ~ & ~ & ~ & ~ &
        ~ & \frac{12 E \cdot I_z}{l_e^3} & 0 & 0 & 0 & -\frac{6 E \cdot I_z}{l_e^2} \\
        %% line 9
        ~ & ~ & ~ & \text{sym.} & ~ & ~ &
        ~ & ~ & \frac{12 E \cdot I_y}{l_e^3} & 0 & \frac{6 E \cdot I_y}{l_e^2} & 0 \\
        %% line 10
        ~ & ~ & ~ & ~ & ~ & ~ &
        ~ & ~ & ~ & \frac{G \cdot J}{l_e} & 0 & 0 \\
        %% line 11
        ~ & ~ & ~ & ~ & ~ & ~ &
        ~ & ~ & ~ & ~ & \frac{4 E \cdot I_y}{l_e} & 0 \\
        %% line 12
        ~ & ~ & ~ & ~ & ~ & ~ &
        ~ & ~ & ~ & ~ & ~ & \frac{4 E \cdot I_z}{l_e} \\
    \end{bmatrix}

The stiffness matrix for a *Timoshenko beam element* which accounts for shear deformations can be found in [CMPW02]_, [Prze85]_. Assuming that the mass is concentrated on the *elastic axis*, the consistent *element mass matrix* is (c.f. [Prze85]_)

.. math::
    :label: eq_element_mass_matrix

    \mathbf{M}_\text{e,dist,loc} =
    \frac{\varrho \cdot A \cdot l_e}{420}
    \begin{bmatrix}
        %% line 1
        140 & 0 & 0 & 0 & 0 & 0 &
        70 & 0 & 0 & 0 & 0 & 0 \\
        %% line 2
        ~ & 156 & 0 & 0 & 0 & 22 \cdot l_e &
        0 & 54 & 0 & 0 & 0 & -13 \cdot l_e \\
        %% line 3
        ~ & ~ & 156 & 0 & -22 \cdot l_e & 0 &
        0 & 0 & 54 & 0 & 13 \cdot l_e & 0 \\
        %% line 4
        ~ & ~ & ~ & \frac{140 \cdot I_x}{A} & 0 & 0 &
        0 & 0 & 0 & 70 \cdot \frac{I_x}{A} & 0 & 0 \\
        %% line 5
        ~ & ~ & ~ & ~ & 4 \cdot l_e^2 & 0 &
        0 & 0 & -13 \cdot l_e & 0 & -3 \cdot l_e^2 & 0 \\
        %% line 6
        ~ & ~ & ~ & ~ & ~ & 4 \cdot l_e^2 &
        0 & 13 \cdot l_e & 0 & 0 & 0 & -3 \cdot l_e^2 \\
        %% line 7
        ~ & ~ & ~ & ~ & ~ & ~ &
        140 & 0 & 0 & 0 & 0 & 0 \\
        %% line 8
        ~ & ~ & ~ & ~ & ~ & ~ &
        ~ & 156 & 0 & 0 & 0 & -22 \cdot l_e \\
        %% line 9
        ~ & ~ & ~ & \text{sym.} & ~ & ~ &
        ~ & ~ & 156 & 0 & 22 \cdot l_e & 0 \\
        %% line 10
        ~ & ~ & ~ & ~ & ~ & ~ &
        ~ & ~ & ~ & \frac{140 \cdot I_x}{A} & 0 & 0 \\
        %% line 11
        ~ & ~ & ~ & ~ & ~ & ~ &
        ~ & ~ & ~ & ~ & 4 \cdot l_e^2 & 0 \\
        %% line 12
        ~ & ~ & ~ & ~ & ~ & ~ &
        ~ & ~ & ~ & ~ & ~ & 4 \cdot l_e^2 \\
    \end{bmatrix}

where :math:`I_x` denotes the polar moment of inertia. The effect of shear deformations can be accounted for in the mass matrix which is shown by Przemieniecki [Prze85]_. Additional *point masses* can be lumped into specific nodes. Consider two masses, :math:`m_1` and :math:`m_2`, assigned to nodes 1 and 2 of an element, respectively. Disregarding rotational inertia, the *element point mass matrix* becomes

.. math::
    :label: eq_element_pointmass_matrix

    & \mathbf{M}_\text{e,point,loc} =
    \begin{bmatrix}
        \mathbf{M}_{m_1} & \mathbf{0} & \mathbf{0} & \mathbf{0} \\
        \mathbf{0} & \mathbf{0} & \mathbf{0} & \mathbf{0} \\
        \mathbf{0} & \mathbf{0} & \mathbf{M}_{m_2} & \mathbf{0} \\
        \mathbf{0} & \mathbf{0} & \mathbf{0} & \mathbf{0} \\
    \end{bmatrix} \\
    &\text{where}~
    \mathbf{M}_{m_1} =
    \begin{bmatrix}
        {m_1} & 0 & 0 \\
        0 & {m_1} & 0 \\
        0 & 0 & {m_1}
    \end{bmatrix}
    , ~
    \mathbf{M}_{m_2} =
    \begin{bmatrix}
        {m_2} & 0 & 0 \\
        0 & {m_2} & 0 \\
        0 & 0 & {m_2}
    \end{bmatrix}

where the zero matrices are of size :math:`3 \times 3`. The final element mass matrix is given as the sum :math:`\mathbf{M}_\text{e,loc} = \mathbf{M}_\text{e,dist,loc} + \mathbf{M}_\text{e,point,loc}`.

Generally, loads may be formulated as being concentrated on a specific node or as being distributed over the length of the element. Distributed loads will eventually be translated into equivalent (concentrated) nodal loads as a result of the Galerkin method. Thus, the load :math:`\mathbf{f}_\text{e,loc}` acting on an element can be written as a sum of concentrated loads :math:`\mathbf{f}_\text{e,conc,loc}` and distributed loads :math:`\mathbf{f}_\text{e,dist,loc}`, forming the *element load vector* (c.f. [AnNi08]_).

.. math::
    :label: eq_element_load_vector

    \mathbf{f}_\text{e,loc} = \mathbf{f}_\text{e,dist,loc} + \mathbf{f}_\text{e,conc,loc}
    \begin{pmatrix}
    q_x \cdot l_e / 2 \\
    q_y \cdot l_e / 2 - m_z \\
    q_z \cdot l_e / 2 + m_y \\
    m_x \cdot l_e / 2 \\
    - q_z \cdot l_e^2 / 12\\
    q_y \cdot l_e^2 / 12\\
    q_x \cdot l_e / 2 \\
    q_y \cdot l_e / 2  + m_z\\
    q_z \cdot l_e / 2 - m_y \\
    m_x \cdot l_e / 2 \\
    q_z \cdot l_e^2 / 12\\
    - q_y \cdot l_e^2 / 12\\
    \end{pmatrix}
    %%
    +
    %%
    \begin{pmatrix}
    F_{x,1} \\
    F_{y,1} \\
    F_{z,1} \\
    M_{x,1} \\
    M_{y,1} \\
    M_{z,1} \\
    F_{x,2} \\
    F_{y,2} \\
    F_{z,2} \\
    M_{x,2} \\
    M_{y,2} \\
    M_{z,2} \\
    \end{pmatrix}


The distributed loads (:math:`q_x`, :math:`q_y`, :math:`q_z`, :math:`m_x`, :math:`m_y` and :math:`m_z` as defined in :ref:`sec_theory_introduction`) are assumed to be *constant* over the length of the element. Therefore, it may be necessary to use a finer discretisation if varying distributed loads are to be modelled accurately.

Transformation into the global system
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

So far, the element tensors have been formulated in the element *local* coordinate system. In order to assemble a global system of equations reflecting the full structure it is first necessary to transform the element tensors using a transformation matrix :math:`\mathbf{T}`, given as (c.f. [CMPW02]_, [YoBS12]_)

.. math::
    :label: eq_element_transformation_matrix

    \mathbf{T} =
    \begin{bmatrix}
        \boldsymbol{\Lambda} & \mathbf{0} & \mathbf{0} & \mathbf{0} \\
        \mathbf{0} & \boldsymbol{\Lambda} & \mathbf{0} & \mathbf{0} \\
        \mathbf{0} & \mathbf{0} & \boldsymbol{\Lambda} & \mathbf{0} \\
        \mathbf{0} & \mathbf{0} & \mathbf{0} & \boldsymbol{\Lambda} \\
    \end{bmatrix}
    %%
    \quad \text{where} \quad
    %%
    \boldsymbol{\Lambda} =
    \begin{bmatrix}
        l_x & m_x & n_x \\
        l_y & m_y & n_y \\
        l_z & m_z & n_z \\
    \end{bmatrix}

and where :math:`l_\text{i}`, :math:`m_\text{i}` and :math:`n_\text{i}` (:math:`i = x, y, z`) are direction cosines defined by

.. math::
    :label: eq_lmn_direction_cosines

    \begin{matrix}
        l_x = \cos \Phi_\text{xX}, & \quad & m_x = \cos \Phi_\text{xY}, & \quad & n_x = \cos \Phi_\text{xZ} \\
        l_y = \cos \Phi_\text{yX}, & \quad & m_y = \cos \Phi_\text{yY}, & \quad & n_y = \cos \Phi_\text{yZ} \\
        l_z = \cos \Phi_\text{zX}, & \quad & m_z = \cos \Phi_\text{zY}, & \quad & n_z = \cos \Phi_\text{zZ}
    \end{matrix}

where :math:`\Phi_{\text{i}\text{j}}` is the angle between a local axis :math:`i` and a global axis :math:`j` (:math:`i = x, y, z` and :math:`j = X, Y, Z`) as illustrated in :numref:`fig_direction_cosines`.

.. _fig_direction_cosines:
.. figure:: ../_static/images/theory/direction_cosines.svg
   :width: 300 px
   :alt: Direction cosines
   :align: center

   The orientation of the local :math:`x`-axis with respect to the global coordinate system is defined by angles :math:`\Phi_\text{xX}`, :math:`\Phi_\text{xY}` and :math:`\Phi_\text{xZ}` (modified from [YoBS12]_)

Using the transformation matrix, the *element* stiffness-, mass- and load tensors can be transformed into the *global* coordinate system (subscript *glob*).

.. math::
    :label: eq_element_stiffness_matrix_glob

    \mathbf{K}_\text{e,glob} = \mathbf{T}^T \cdot \mathbf{K}_\text{e,loc} \cdot \mathbf{T}

.. math::
    :label: eq_element_mass_matrix_glob

    \mathbf{M}_\text{e,glob} = \mathbf{T}^T \cdot \mathbf{M}_\text{e,loc} \cdot \mathbf{T}

.. math::
    :label: eq_element_load_vector_global_glob

    \mathbf{f}_\text{e,glob} = \mathbf{T}^T \cdot \mathbf{f}_\text{e,loc}

Assembly of the global system of equations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The entire structure system can finally be *assembled* into a system of equations, now consistently formulated with respect to the global coordinate system. A full structure (here referred to as frame) is made up of individual beams (substructures). :numref:`fig_matrix_assembly` and :numref:`fig_vector_assembly` illustrates how the *global stiffness matrix* :math:`\mathbf{K}`, the *global mass matrix* :math:`\mathbf{M}` and the *global load vector* :math:`\mathbf{F}` are assembled based on the transformed element matrices, :eq:`eq_element_stiffness_matrix_glob`, :eq:`eq_element_mass_matrix_glob`, :eq:`eq_element_load_vector_global_glob`.

.. _fig_matrix_assembly:
.. figure:: ../_static/images/theory/matrix_assembly.svg
   :width: 250 px
   :alt: Matrix assembly
   :align: center

   Matrix assembly

.. _fig_vector_assembly:
.. figure:: ../_static/images/theory/vector_assembly.svg
   :width: 120 px
   :alt: Vector assembly
   :align: center

   Vector assembly

Assembly of global tensors. The element matrices and vectors are of size :math:`12 \times 12` and :math:`12 \times 1`, respectively. Potential connections between individual beams (e.g. rigid connections) are defined separately through boundary conditions.

A static equilibrium is described by

.. math::
    :label: eq_fem_static_with_gravity

    \mathbf{K} \cdot \mathbf{U} = \mathbf{F} + \mathbf{F}_\text{accel} \qquad \text{with} \quad \mathbf{F}_\text{accel} := \mathbf{M} \cdot \mathbf{A}

where :math:`\mathbf{U}` is the *global vector of nodal deformations* (nodal deformations with respect to the global system). The additional term :math:`\mathbf{F}_\text{accel}` allows to take loads due to gravity or due to quasi-steady flight manoeuvres into account, when the acceleration is known (inertia relief method [Wijk04]_). The (translational) acceleration vector is

.. math::
    :label: eq_accel_vector

    \mathbf{A} = \left( a_x, a_y, a_z, 0, 0, 0, a_x, a_y, a_z, 0, 0, 0, \dots \right)^T

where :math:`a_x`, :math:`a_y` and :math:`a_z` are accelerations in :math:`X`-, :math:`Y`- and :math:`Z`-directions of the global coordinate system. Gravity in :math:`Z`-direction, for instance, can be modelled by setting :math:`a_x = a_y = 0` and :math:`a_z = -g` with :math:`g` being the gravitational acceleration. By performing the multiplication :math:`\mathbf{M} \cdot \mathbf{A}` it can be shown that the weight of each element is modelled as a constant distributed load, and analogous to eq. :eq:`eq_element_load_vector`, divided between the two nodes of the element.

Boundary conditions
~~~~~~~~~~~~~~~~~~~

Equation :eq:`eq_fem_static_with_gravity` is to be solved for the global vector of nodal deformations :math:`\mathbf{U}`. Without fixing the structure in space, :math:`\mathbf{K}` is singular and the system of equations cannot be uniquely solved. To find a unique solution, boundary conditions have to be applied. Linear constraints imposed on the structure can be formulated as :math:`\mathbf{B} \cdot \mathbf{U} = \mathbf{b}` where the matrix :math:`\mathbf{B}` and the vector :math:`\mathbf{b}` contain constants. This formulation can be used to impose both *single point constraints* (e.g. setting single |dof| to known values, often zero) as well as *multipoint constraints* (e.g. a rigid connector between two nodes) [CMPW02]_. As shown in [CMPW02]_, Lagrange's method of undetermined multipliers can be used to formulate a system of equations for the structure including the applied boundary conditions.

.. math::
    :label: eq_static_analysis

    \begin{bmatrix}
        \mathbf{K} & \mathbf{B} \\
        \mathbf{B}^T & \mathbf{0}
    \end{bmatrix}
    \cdot
    \begin{pmatrix}
        \mathbf{U} \\
        \boldsymbol{\lambda}
    \end{pmatrix}
    =
    \begin{pmatrix}
        \mathbf{F} + \mathbf{F}_\text{accel} \\
        \mathbf{0}
    \end{pmatrix}

Here, :math:`\boldsymbol{\lambda}` is a vector with the Lagrange multipliers of length equal to the number of linear constraints. Euquation :eq:`eq_static_analysis` is solved for :math:`\mathbf{U}` and :math:`\boldsymbol{\lambda}`, where the Lagrange multipliers may be interpreted as forces of constraint [CMPW02]_.

.. note::

    This summary is based on/copied from [Dett19]_ with the authors permission.
