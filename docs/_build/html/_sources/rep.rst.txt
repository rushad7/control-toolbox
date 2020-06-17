======================
System Representation
======================

Currently, systems can be defined by Transfer Functions. Support for State Space models will be added in a future update.

Transfer Functions
===================

A Transfer Functions is the Laplace Transform of the ratio of output to input, and are mathematically described as:

.. figure:: /shared_images/tf.png
   :align: center

To define a system in terms of a Transfer Function, use the `TransferFunction` class.
::
	>>> import control
	>>> s = control.TransferFunction(num, den)

Here `num` and `den` can be lists or numpy arrays


State Space Models
===================

Space State models are mathamatically described as:

.. figure:: /shared_images/ss.png
   :align: center

To define a system as Space State model, use the `StateSpace` class.
::
	>>> import control
	>>> s = control.StateSpce(A,B,C,D)

Here, A,B,C,D are ndarrays.

.. note:: Although you can define the system in any form, currently most functionality is suited for the Transfer Function form. Therefore, you need to convert the State Space model to the Transfer Function model first using the `StateSpace.convertTF()` method. Direct support for State Space modelswill be added in a future update.
