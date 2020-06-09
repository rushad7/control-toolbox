======================
System Representation
======================

Currently, systems can be defined by Transfer Functions. Support for State Space models will be added in a future update.

Transfer Functions
===================

A Transfer Functions is the Laplace Transform of the ratio of output to input, and are mathematically described as:
.. math::

  G(s) = \frac{\text{num}(s)}{\text{den}(s)}
       = \frac{a_0 s^m + a_1 s^{m-1} + \cdots + a_m}
              {b_0 s^n + b_1 s^{n-1} + \cdots + b_n}

To define a system in terms of a Transfer Function, use the `TransferFunction` class.
::
 >>> import control
 >>> s = control.TransferFunction(num, den)

For example:
::
 >>> import control
 >>> sys = control.TransferFunctin([1], [1,2,3])
 >>> sys.response("step", time_period=10, sample_response=0.01)
 >>> sys.stability()
 >>> sys.pzplot()
 >>> sys.parameters()
 >>> sys.display()
