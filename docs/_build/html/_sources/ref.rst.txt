====================
Function Reference
====================

The following table lists the classes and methods that can be used to model and simulate various systems and control strategies.

System Definition
*****************
.. csv-table:: 
   :header: "Class", "Description"
   :widths: 40, 40

   "`TransferFunction(num, den)`", "Creates a Transfer Function system object"
   "`StateSpace(A,B,C,D)`", "Creates a State Space system object"

Transfer Function methods
***************************
.. csv-table:: 
   :header: "Method", "Description"
   :widths: 40, 40

   "`display()`", "Displays the Transfer Function system"
   "`parameters(settling_time_tolerance=0.02)`", "Returns the parameters of the system"
   "`response(input_type, time_period=10, sample_time=0.05, ret=False, show=True)`", "Returns the time domain response on the system"
   "`pzplot(ret=True)`", "Plots the Pole-Zero plot of the system and return poles and zeros"
   "`stability()`", "Returns the stability of the system"
   "`rootlocus(tf, gain_range=10.0)`", "Returns Root Locus of the system"

State Space methods
********************
.. csv-table:: 
   :header: "Method", "Description"
   :widths: 40, 40

   "`display()`", "Displays the State Space system"
   "`convertTF()`", "Converts State Space model to Transfer Function"
   "`contr()`", "Controllability of the system"
   "`obs()`", "Observability of the system"

System Connections
*******************
.. csv-table:: 
   :header: "Method", "Description"
   :widths: 40, 40

   "`feedback( G, H=1.0, feedback_type=""negative"")`", "Feedback for the system"
   "`reduce.series(tf1, *tfn)`", "Return the series connection (tfn * …"
   "`reduce.parallel(tf1, *tfn)`", "Return the parallel connection (tfn + …"

PID Control
************
.. csv-table:: 
   :header: "Method", "Description"
   :widths: 40, 40

   "`PID(Kp, Ki, Kd, tf)`", "Define PID system"
   "`response(input_type, time_period=10, sample_time=0.05, ret=False, show=True)`", "Return the response of the system after PID control"
   "`tune(input_type=""step"", set_point=1, num_itr=70, rate=0.00000000001)`", "Tune the PID coefficients"
   "`display()`", "Display the PID block"
   "`reduced_tf`", "Displays the reduced Transfer Function (Controller + Plant)"

System Connections
*******************
.. csv-table:: 
   :header: "Method", "Description"
   :widths: 40, 40

   "`feedback( G, H=1.0, feedback_type=""negative"")`", "Feedback for the system"
   "`reduce.series(tf1, *tfn)`", "Return the series connection (tfn * …"
   "`reduce.parallel(tf1, *tfn)`", "Return the parallel connection (tfn + …"

Frequency Domain
*****************

.. csv-table:: 
   :header: "Method", "Description"
   :widths: 40, 40

   "`bode.freqresp(tf)`", "Returns the Frequency Response of the system"
   "`bode.bode(tf)`", "Returns the Bode Plot of the system"

