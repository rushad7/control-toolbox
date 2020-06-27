======================
System Representation
======================

Systems can be defined by Transfer Functions and State Space models. Both system representations provide near identical utility.

Transfer Functions
===================

A Transfer Function is the Laplace Transform of the ratio of output to input, and are mathematically described as:

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

.. note:: Although you can define a system in any of the above form, few features are suited only for a particular representation. Therefore, if a particular method is needed and is not provided for the given system, you need to convert the system model first using the `convert2TF()` or `convert2SS()` method. Direct support for these methods will be added in a future update.
