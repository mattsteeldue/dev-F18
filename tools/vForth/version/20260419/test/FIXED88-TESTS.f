\
\ FIXED-TESTS.f
\

NEEDS FIXED88

MARKER TESTING-TASK

NEEDS TESTING

TESTING \ ZX Spectrum Floating-Point interface

DECIMAL

T{  3 INT>8.8   4 INT>8.8   F-       ->   -1 INT>8.8  }T
T{  3 INT>8.8   4 INT>8.8   F*       ->   12 INT>8.8  }T
T{  3 INT>8.8   4 INT>8.8   F/       ->    1 INT>8.8  }T
T{  3 INT>8.8   4 INT>8.8   F+       ->    7 INT>8.8  }T
T{  3 INT>8.8   4 INT>8.8   FNEGATE  ->    3 INT>8.8  }T
T{  3 INT>8.8   4 INT>8.8   FSGN     ->    3 INT>8.8  }T
T{  3 INT>8.8   4 INT>8.8   FABS     ->    3 INT>8.8  }T
T{  3 INT>8.8   4 INT>8.8   F/MOD    ->    3 INT>8.8  }T
T{  3 INT>8.8   4 INT>8.8   F**      ->    9 INT>8.8  }T
                                        
T{  1. FLN               ->    0.              }T
T{  PI FEXP  FLN         ->    PI              }T
T{  PI FSQRT 2DUP F*     ->    PI              }T
T{  PI FINT              ->    3.              }T

T{  0. FSIN              ->    0.              }T
T{  0. FCOS              ->    2. 2. F/        }T
T{  PI FTAN              ->    0.              }T
T{  1. FASIN             ->    PI 2. F/        }T
T{  1. FACOS             ->    0.              }T 
T{  1. FATAN 2. F*       ->    PI 2. F/ 

                                        
T{  60. DEG>RAD          ->    PI 3. F/        }T
T{  PI  RAD>DEG          ->  360. 2. F/        }T


