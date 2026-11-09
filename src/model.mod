// ** PLEASE ONLY CHANGE THIS FILE WHERE INDICATED **
// In particular, do not change the names of the OPL variables.

int N = ...;
int L = ...;
int U = ...;
int T = ...;

int P[1..N] = ...;
int E[1..N] = ...;

// Define here your decision variables and
// any other auxiliary OPL variables you need.
// You can run an execute block if needed.

//>>>>>>>>>>>>>>>>

dvar boolean A[1..N]; // A[i]: is machine active at moment i?

//<<<<<<<<<<<<<<<<

// You can run an execute block if needed.

execute {

//>>>>>>>>>>>>>>>>

  

//<<<<<<<<<<<<<<<<
}

minimize sum(i in 1..N) E[i] * A[i];

//>>>>>>>>>>>>>>>>
// ...
//<<<<<<<<<<<<<<<<

subject to {

    // Write here the constraints.

    //>>>>>>>>>>>>>>>>

    // Constraint 1 (min profit)
    T <= sum(i in 1..N) P[i] * A[i];

    // Constraint 2 (minimum run length)
    

    // Constraint 3 (maximum run length)
    forall (i in 1..N-U)
      U >= sum(j in i..i+U) A[j];

    //<<<<<<<<<<<<<<<<
}

// You can run an execute block if needed.

execute {

//>>>>>>>>>>>>>>>>
  
  var time_a = -1;
  
  for (var i = 1; i <= N; i++) {
    if (time_a == -1 && A[i] > 0.5) {
      time_a = i;                       // a run starts
    } else if (time_a != -1 && A[i] < 0.5) {
      writeln(time_a, " ", i - 1);      // a run ends
      time_a = -1;                      // reset
    }
  }
  
  if (time_a != -1)                     // run that reaches the end
    writeln(time_a, " ", N);

//<<<<<<<<<<<<<<<<
}
