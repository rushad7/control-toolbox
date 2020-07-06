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

Transfer Function Methods
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

State Space Methods
********************
.. csv-table:: 
   :header: "Method", "Description"
   :widths: 40, 40

   "`display()`", "Displays the State Space system"
   "`convert2TF()`", "Converts State Space model to Transfer Function"
   "`contr()`", "Controllability of the system"
   "`obs()`", "Observability of the system"
   "`stability()`", "Stability of the system"
   "`eigplot(ret=True)`", "Plots eigenvalues/poles of system"
   "`StateResponse(t, initial_cond, u, ret=False, show=True)`", "Returns and plots state response"
   "`OutputResponse(t, initial_cond, u, ret=False, show=True)`", "Returns and plots output response"

System Connections
*******************
.. csv-table:: 
   :header: "Method", "Description"
   :widths: 40, 40

   "`feedback( G, H=1.0, feedback_type=""negative"")`", "Creates a Feedback Object"
   "`reduce.series(tf1, *tfn)`", "Return the series connection (tfn * …"
   "`reduce.parallel(tf1, *tfn)`", "Return the parallel connection (tfn + …"

Frequency Domain Analysis
*************************

.. csv-table:: 
   :header: "Method", "Description"
   :widths: 40, 40

   "`bode.freqresp(tf)`", "Returns the Frequency Response of the system"
   "`bode.bode(tf)`", "Returns the Bode Plot of the system"

PID Controller Design
**********************
.. csv-table:: 
   :header: "Method", "Description"
   :widths: 40, 40

   "`PID(Kp, Ki, Kd, tf)`", "Creates a PID object"
   "`response(input_type, time_period=10, sample_time=0.05, ret=False, show=True)`", "Return the response of the system after PID control"
   "`tune(input_type=""step"", set_point=1, num_itr=70, rate=0.00000000001, lambd=0.7)`", "Tune the PID coefficients"
   "`display()`", "Display the PID block"
   "`reduced_tf`", "Displays the reduced Transfer Function (Controller + Plant)"

State Feedback Design
*********************
.. csv-table:: 
   :header: "Method", "Description"
   :widths: 40, 40

   "`StateFeedback(ss)`", "Creates a StateFeedback object"
   "`solve(roots)`", "Calculates the State Feedback gain matrix"
   "`model(k_ref=1)`", "Retruns StateSpace object after applying State Feedback"

State Observer Design
*********************
.. csv-table:: 
  :header: "Method", "Description"
  :widths: 40, 40

  "`StateObserver(ss)`", "Creates StateObserver object"
  "`solve(roots)`", "Calculates the State Observer gain matrix"
  "`model(k_ref=1)`", "Retruns the StateSpace object after applying State Observervation"

Linear Quadratic Regulator(LQR)
*******************************
.. csv-table:: 
  :header: "Method", "Description"
  :widths: 40, 40
  
  "`LQR(ss, Q, R, N)`", "Creates an LQR object"
  "`solve()`", "Calculates the optimal gain matrix"
  "`model()`", "Returns the StateSpace object after applying State Observation"

Kalman Filter / Linear Quadratic Estimator(LQE)
***********************************************
.. csv-table:: 
  :header: "Method", "Description"
  :widths: 40, 40
  
  "`KalmanFilter(ss, Q, R, P=None, x0=None)`", "Creates a KalmanFilter object"
  "`predict(u = 0):`", "Predict next state"
  "`update(z):`", "Update Predictions"
  "`solve(measurements, ret_k=False, ret_x=False):`", "Returns the Predictions, Kalman Gain, and States of the system"
